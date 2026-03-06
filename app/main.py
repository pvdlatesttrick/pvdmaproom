"""Flask application factory and routes."""
from __future__ import annotations

import logging
import os
import threading
import time
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

# In-memory cache for /api/stories to avoid repeated DB hits (60s TTL).
_stories_cache: dict = {"stories": None, "ts": 0.0, "limit": None, "year": None}
STORIES_CACHE_TTL = 60

from app.ai_summary import summarize_country, summarize_story
from app.chat import chat as chat_reply
from app.db import get_all_countries_baseline, get_country_detail, get_stories, get_db_path, get_total_mapped_story_count, init_db
from app.ingest import run_ingest
from app.isw_frontlines import ISW_FRONTLINES_GEOJSON

# Optional features: log at startup so deploy logs show what's available.
def _log_optional_features() -> None:
    log = logging.getLogger(__name__)
    has_openai = bool(os.environ.get("OPENAI_API_KEY", "").strip())
    has_groq = bool(os.environ.get("GROQ_API_KEY", "").strip())
    if not has_openai and not has_groq:
        log.warning(
            "Neither OPENAI_API_KEY nor GROQ_API_KEY is set. Location inference will not run: "
            "stories that cannot be geocoded will get no pins. Set one of these in Render Environment "
            "(e.g. GROQ_API_KEY from console.groq.com) so pins appear on the map."
        )
    elif not has_openai:
        log.info("OPENAI_API_KEY not set; using GROQ for AI summary, titles, chat, and location inference.")
    if not os.environ.get("NYT_API_KEY", "").strip():
        log.info("NYT_API_KEY not set: NYT Top Stories API disabled; RSS still used for NYT.")


def create_app() -> Flask:
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Ensure DB tables exist before first request.
    init_db()
    _log_optional_features()

    # Ingest state for async ingest and polling (single-threaded; one ingest at a time).
    _ingest_lock = threading.Lock()
    _ingest_state = {"running": False, "last_completed_at": None, "last_mapped_count": 0, "last_error": None}

    def _run_ingest_and_log() -> None:
        with _ingest_lock:
            if _ingest_state["running"]:
                return
            _ingest_state["running"] = True
            _ingest_state["last_error"] = None
        try:
            run_ingest()
            n = get_total_mapped_story_count()
            with _ingest_lock:
                _ingest_state["last_completed_at"] = datetime.now(timezone.utc).isoformat()
                _ingest_state["last_mapped_count"] = n
            logging.getLogger(__name__).info("Background ingest finished: %s mapped stories", n)
        except Exception as e:
            with _ingest_lock:
                _ingest_state["last_error"] = str(e)
            logging.getLogger(__name__).exception("Background ingest failed: %s", e)
        finally:
            with _ingest_lock:
                _ingest_state["running"] = False

    def _start_ingest_if_idle() -> bool:
        with _ingest_lock:
            if _ingest_state["running"]:
                return False
        threading.Thread(target=_run_ingest_and_log, daemon=True).start()
        return True

    threading.Thread(target=_run_ingest_and_log, daemon=True).start()

    # Scheduled re-ingest every 45 minutes and keep-alive ping so Render free tier doesn't spin down.
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        import urllib.request
        scheduler = BackgroundScheduler()
        scheduler.add_job(lambda: threading.Thread(target=_run_ingest_and_log, daemon=True).start(), "interval", minutes=45, id="ingest")
        port = os.environ.get("PORT", "10000")
        def _ping():
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{port}/ping", timeout=5)
            except Exception as e:
                logging.getLogger(__name__).debug("Keep-alive ping failed: %s", e)
        scheduler.add_job(_ping, "interval", minutes=14, id="keepalive")
        scheduler.start()
        logging.getLogger(__name__).info("Scheduler started: re-ingest every 45 min, keep-alive every 14 min.")
    except ImportError:
        logging.getLogger(__name__).warning("APScheduler not installed; no scheduled re-ingest.")

    @app.get("/ping")
    def ping():
        """Lightweight route for keep-alive pings so Render free tier does not spin down."""
        return jsonify({"ok": True})

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/historical")
    def historical():
        """Historical Map view: borders and pins keyed by year; year/borders controls apply here only."""
        return render_template("historical.html")

    @app.get("/api/stories/meta")
    def api_stories_meta():
        """Lightweight endpoint: count and last_updated only (<50ms). Use before fetching full stories."""
        with _ingest_lock:
            last_completed = _ingest_state.get("last_completed_at")
            count = _ingest_state.get("last_mapped_count")
        if count is None:
            count = get_total_mapped_story_count()
        return jsonify({"count": count, "last_updated": last_completed})

    @app.get("/api/stories")
    def api_stories():
        limit_param = request.args.get("limit", "").strip()
        limit = 50
        if limit_param:
            try:
                limit = max(1, min(500, int(limit_param)))
            except ValueError:
                pass
        year_param = request.args.get("year", "").strip()
        year: int | None = None
        if year_param:
            try:
                year = int(year_param)
            except ValueError:
                pass
        now = time.time()
        if (
            _stories_cache["stories"] is not None
            and _stories_cache["limit"] == limit
            and _stories_cache["year"] == year
            and (now - _stories_cache["ts"]) < STORIES_CACHE_TTL
        ):
            return jsonify(_stories_cache["stories"])
        stories = get_stories(limit=limit, year=year)
        if year is not None:
            from app.historical_events import fetch_historical_events
            try:
                historical = fetch_historical_events(year)
                seen_urls = {s.get("url") for s in stories}
                for h in historical:
                    if h.get("url") not in seen_urls:
                        stories.append(h)
                        seen_urls.add(h.get("url"))
            except Exception as e:
                logging.getLogger(__name__).warning("Historical events fetch failed: %s", e)
        _stories_cache["stories"] = stories
        _stories_cache["ts"] = now
        _stories_cache["limit"] = limit
        _stories_cache["year"] = year
        return jsonify(stories)

    @app.get("/api/status")
    def api_status():
        """Return mapped story count and DB path so you can confirm the backend has pins."""
        import os
        db_path = get_db_path()
        count = get_total_mapped_story_count()
        return jsonify({
            "mapped_story_count": count,
            "db_path": db_path,
            "db_exists": os.path.isfile(db_path),
        })

    @app.post("/api/ingest")
    def api_ingest():
        """Start ingest in background. Poll GET /api/ingest-status for progress."""
        if not _start_ingest_if_idle():
            return jsonify({"status": "running", "message": "Ingest already in progress. Poll GET /api/ingest-status."})
        return jsonify({"status": "started", "message": "Ingest running. Poll GET /api/ingest-status for progress."})

    @app.get("/api/ingest-status")
    def api_ingest_status():
        """Return current ingest state for polling (no blocking)."""
        with _ingest_lock:
            return jsonify({
                "status": "running" if _ingest_state["running"] else "idle",
                "mapped_story_count": get_total_mapped_story_count(),
                "last_completed_at": _ingest_state.get("last_completed_at"),
                "last_error": _ingest_state.get("last_error"),
            })

    @app.get("/api/country")
    def api_country():
        name = (request.args.get("name") or "").strip()
        if not name:
            return jsonify({"error": "country name is required"}), 400
        year_param = request.args.get("year", "").strip()
        year = None
        if year_param:
            try:
                year = int(year_param)
            except ValueError:
                pass
        return jsonify(get_country_detail(name, year=year))

    @app.get("/api/isw-frontlines")
    def api_isw_frontlines():
        """Return GeoJSON for ISW-style front lines (Conflicts map overlay)."""
        return jsonify(ISW_FRONTLINES_GEOJSON)

    @app.post("/api/chat")
    def api_chat():
        """Answer a question using map articles and data; aligns with WSJ, Economist, Hudson, AEI, The Dispatch."""
        data = request.get_json(silent=True) or {}
        message = (data.get("message") or "").strip()
        if not message:
            return jsonify({"error": "message is required"}), 400
        map_key = (data.get("map_key") or "").strip() or None
        country = (data.get("country") or "").strip() or None
        stories = get_stories(limit=250)
        country_baseline = get_all_countries_baseline()
        reply = chat_reply(
            user_message=message,
            stories=stories,
            map_key=map_key,
            country=country,
            country_baseline=country_baseline,
        )
        if reply is None:
            return jsonify({
                "error": "Chat unavailable. Set GROQ_API_KEY (free at console.groq.com) or OPENAI_API_KEY in your Render service Environment Variables."
            }), 503
        return jsonify({"reply": reply})

    @app.post("/api/ai-summary")
    def api_ai_summary():
        """Return an AI summary for a country or a story. Requires GROQ_API_KEY or OPENAI_API_KEY."""
        data = request.get_json(silent=True) or {}
        kind = (data.get("type") or "").strip().lower()
        if kind == "country":
            country_name = (data.get("country") or "").strip()
            if not country_name:
                return jsonify({"error": "country name is required"}), 400
            map_key = (data.get("map_key") or "").strip() or None
            year_val = data.get("year")
            year_int: int | None = None
            if year_val is not None:
                try:
                    year_int = int(year_val)
                except (TypeError, ValueError):
                    pass
            try:
                detail = get_country_detail(country_name)
                facts = None
                if detail.get("facts"):
                    facts = {k: v for k, v in detail["facts"].items() if v}
            except Exception:
                facts = None
            summary_text = summarize_country(country_name, facts, map_key=map_key, year=year_int)
        elif kind == "story":
            title = (data.get("title") or "").strip()
            summary = (data.get("summary") or "").strip()
            if not title and not summary:
                return jsonify({"error": "title or summary is required"}), 400
            summary_text = summarize_story(
                title=title,
                summary=summary,
                country=(data.get("country") or "").strip() or None,
                source=(data.get("source") or "").strip() or None,
            )
        else:
            return jsonify({"error": "type must be 'country' or 'story'"}), 400
        if summary_text is None:
            return jsonify({
                "error": "AI summary unavailable. Set GROQ_API_KEY (free at console.groq.com) or OPENAI_API_KEY in your Render service Environment Variables."
            }), 503
        return jsonify({"summary": summary_text})

    return app
