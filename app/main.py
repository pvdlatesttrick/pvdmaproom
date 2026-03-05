"""Flask application factory and routes."""

from __future__ import annotations

import logging
import threading
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, send_file

from app.ai_summary import summarize_country, summarize_story
from app.chat import chat as chat_reply
from app.db import get_country_detail, get_stories, get_db_path, get_total_mapped_story_count, init_db
from app.ingest import run_ingest
from app.isw_frontlines import ISW_FRONTLINES_GEOJSON

SOURCE_LOGO_FILES = {
    # User-provided logo assets.
    "economist": Path(
        "/Users/petervandixhoorn/.cursor/projects/Users-petervandixhoorn-Coding-nhlstats-app-static/assets/image-bb397791-72a7-4dcc-b408-c5afa5c5b6dd.png"
    ),
    "washingtonpost": Path(
        "/Users/petervandixhoorn/.cursor/projects/Users-petervandixhoorn-Coding-nhlstats-app-static/assets/image-c2c5b252-df01-4a59-9904-96d65f8737d2.png"
    ),
    "nyt": Path(
        "/Users/petervandixhoorn/.cursor/projects/Users-petervandixhoorn-Coding-nhlstats-app-static/assets/image-18e73cc2-e4ab-494a-802e-f8a37375ae7b.png"
    ),
}


def create_app() -> Flask:
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Ensure DB tables exist before first request.
    init_db()

    def _run_ingest_and_log():
        try:
            run_ingest()
            n = get_total_mapped_story_count()
            logging.getLogger(__name__).info("Background ingest finished: %s mapped stories", n)
        except Exception as e:
            logging.getLogger(__name__).exception("Background ingest failed: %s", e)

    threading.Thread(target=_run_ingest_and_log, daemon=True).start()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/stories")
    def api_stories():
        return jsonify(get_stories())

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
        """Trigger ingest (blocks until complete; can take minutes). Returns mapped count after run."""
        try:
            run_ingest()
            count = get_total_mapped_story_count()
            return jsonify({"status": "completed", "mapped_story_count": count})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.get("/api/country")
    def api_country():
        name = (request.args.get("name") or "").strip()
        if not name:
            return jsonify({"error": "country name is required"}), 400
        return jsonify(get_country_detail(name))

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
        reply = chat_reply(
            user_message=message,
            stories=stories,
            map_key=map_key,
            country=country,
        )
        if reply is None:
            return jsonify({
                "error": "Chat unavailable. In Render: open your pvdmaproom service → Environment (Environment Variables) → Add OPENAI_API_KEY with your OpenAI key."
            }), 503
        return jsonify({"reply": reply})

    @app.get("/api/source-logo/<source_key>")
    def api_source_logo(source_key: str):
        path = SOURCE_LOGO_FILES.get(source_key.strip().lower())
        if path is None or not path.exists():
            abort(404)
        return send_file(path)

    @app.post("/api/ai-summary")
    def api_ai_summary():
        """Return an AI summary for a country or a story. Requires OPENAI_API_KEY."""
        data = request.get_json(silent=True) or {}
        kind = (data.get("type") or "").strip().lower()
        if kind == "country":
            country_name = (data.get("country") or "").strip()
            if not country_name:
                return jsonify({"error": "country name is required"}), 400
            try:
                detail = get_country_detail(country_name)
                facts = None
                if detail.get("facts"):
                    facts = {k: v for k, v in detail["facts"].items() if v}
            except Exception:
                facts = None
            summary_text = summarize_country(country_name, facts)
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
                "error": "AI summary unavailable. In Render: open your pvdmaproom service → Environment (Environment Variables) → Add OPENAI_API_KEY with your OpenAI key."
            }), 503
        return jsonify({"summary": summary_text})

    return app

