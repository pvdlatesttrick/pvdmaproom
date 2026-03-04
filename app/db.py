"""SQLite helpers for stories and geocode cache."""

from __future__ import annotations

import os
import re
import sqlite3
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from app.factbook import normalize_country_name

# Sources considered more popular / widely read for ranking country-panel articles
POPULAR_SOURCES = frozenset({
    "bbc", "bbc_asia", "bbc_africa", "bbc_middle_east",
    "reuters", "nyt", "washingtonpost", "wsj", "economist", "economist_asia", "economist_mea",
    "guardian_world", "guardian_international", "aljazeera", "axios", "politico",
    "dw_world", "abc_news", "cnn", "nbc", "sky_news",
    "on3", "nbcsports", "the_athletic",
    "substack_jamestown", "substack_rochan", "substack_counteroffensive",
    "x_barakravid", "x_clarissaward", "x_richardengel", "x_lynsaddler",
    "x_nickpatonwalsh", "x_borzsandor", "x_ianbremmer",
    "x_rudaw", "x_middleeasteye", "x_kurdistan24",
    "rudaw_english", "middle_east_eye",
    "substack_warwickpowell", "substack_professorbonk",
    "espn_news", "espn_nfl", "espn_nba", "espn_mlb", "espn_nhl", "espn_soccer",
    "espn_ncf", "espn_ncb", "espn_ncaa", "espn_tennis",
    "dispatch", "amnesty", "hrw",
})

def get_db_path() -> str:
    """Return DB path, defaulting to /data/app.db for Docker volume usage."""
    return os.getenv("DB_PATH", "/data/app.db")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_connection() -> sqlite3.Connection:
    """Open a SQLite connection and enable dict-like row access."""
    db_path = get_db_path()
    parent = os.path.dirname(db_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create tables if they do not exist yet."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS stories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                summary TEXT NOT NULL,
                published_at TEXT NOT NULL,
                place TEXT NULL,
                lat REAL NOT NULL,
                lon REAL NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS geocode_cache (
                place TEXT PRIMARY KEY,
                lat REAL NOT NULL,
                lon REAL NOT NULL,
                country TEXT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cia_country_facts (
                country_name TEXT PRIMARY KEY,
                capital TEXT NULL,
                population TEXT NULL,
                gdp_ppp TEXT NULL,
                area_total TEXT NULL,
                government_type TEXT NULL,
                economist_economic_rank TEXT NULL,
                cia_risk_rating TEXT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS country_names (
                english_name TEXT PRIMARY KEY,
                original_name TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS economist_rankings (
                country_name TEXT NOT NULL,
                indicator_key TEXT NOT NULL,
                rank_value INTEGER NULL,
                score_value REAL NULL,
                year TEXT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (country_name, indicator_key)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS article_related_video (
                article_url TEXT PRIMARY KEY,
                video_url TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        # Lightweight migration support for existing DB files.
        if not _has_column(conn, "stories", "country"):
            conn.execute("ALTER TABLE stories ADD COLUMN country TEXT NULL")
        if not _has_column(conn, "geocode_cache", "country"):
            conn.execute("ALTER TABLE geocode_cache ADD COLUMN country TEXT NULL")
        if not _has_column(conn, "cia_country_facts", "economist_economic_rank"):
            conn.execute(
                "ALTER TABLE cia_country_facts ADD COLUMN economist_economic_rank TEXT NULL"
            )
        if not _has_column(conn, "cia_country_facts", "cia_risk_rating"):
            conn.execute("ALTER TABLE cia_country_facts ADD COLUMN cia_risk_rating TEXT NULL")
        _migrate_stories_url_country_unique(conn)
        if not _has_column(conn, "stories", "display_title"):
            conn.execute("ALTER TABLE stories ADD COLUMN display_title TEXT NULL")
        conn.commit()


def _has_column(conn: sqlite3.Connection, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(row["name"] == column for row in rows)


def _migrate_stories_url_country_unique(conn: sqlite3.Connection) -> None:
    """Migrate stories to UNIQUE(url, country) so one story can appear in multiple countries."""
    for name in ("stories", "stories_new"):
        row = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
            (name,),
        ).fetchone()
        if row and row[0] and "UNIQUE(url,country)" in row[0].replace(" ", ""):
            return
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS stories_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            summary TEXT NOT NULL,
            published_at TEXT NOT NULL,
            place TEXT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            created_at TEXT NOT NULL,
            country TEXT NULL,
            UNIQUE(url, country)
        )
        """
    )
    conn.execute(
        """
        INSERT OR IGNORE INTO stories_new
            (id, source, title, url, summary, published_at, place, lat, lon, created_at, country)
        SELECT id, source, title, url, summary, published_at, place, lat, lon, created_at, country
        FROM stories
        """
    )
    conn.execute("DROP TABLE stories")
    conn.execute("ALTER TABLE stories_new RENAME TO stories")


def upsert_story(story: dict[str, Any]) -> None:
    """Insert or update a story by (URL, country) so the same story can appear in multiple countries."""
    country = story.get("country") or ""
    display_title = (story.get("display_title") or "").strip() or None
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO stories (
                source, title, url, summary, published_at, place, country, lat, lon, created_at, display_title
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url, country) DO UPDATE SET
                source = excluded.source,
                title = excluded.title,
                summary = excluded.summary,
                published_at = excluded.published_at,
                place = excluded.place,
                lat = excluded.lat,
                lon = excluded.lon,
                display_title = COALESCE(excluded.display_title, stories.display_title)
            """,
            (
                story["source"],
                story["title"],
                story["url"],
                story["summary"],
                story["published_at"],
                story.get("place"),
                country,
                story["lat"],
                story["lon"],
                _utc_now_iso(),
                display_title,
            ),
        )
        conn.commit()


def _normalize_article_url(url: str) -> str:
    """Normalize article URL for matching (strip fragment, drop UTM/ref, lowercase)."""
    if not url or not url.strip():
        return ""
    parsed = urlparse(url.strip())
    netloc = (parsed.netloc or "").lower()
    path = parsed.path or "/"
    qs = parse_qs(parsed.query, keep_blank_values=False)
    filtered = {k: v for k, v in qs.items() if not (k.lower().startswith("utm_") or k.lower() == "ref")}
    new_query = urlencode(filtered, doseq=True) if filtered else ""
    return urlunparse((parsed.scheme or "https", netloc, path, "", new_query, ""))


def upsert_article_related_video(article_url: str, video_url: str) -> None:
    """Record that a social video (e.g. X post) links to this article — verified relation."""
    key = _normalize_article_url(article_url)
    if not key or not video_url:
        return
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO article_related_video (article_url, video_url, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(article_url) DO UPDATE SET video_url = excluded.video_url, updated_at = excluded.updated_at
            """,
            (key, video_url.strip(), _utc_now_iso()),
        )
        conn.commit()


def get_related_video_urls_batch(article_urls: list[str]) -> dict[str, str]:
    """Return mapping normalized_article_url -> video_url for articles that have a verified related video."""
    if not article_urls:
        return {}
    keys = [k for u in article_urls if (k := _normalize_article_url(u))]
    if not keys:
        return {}
    placeholders = ",".join("?" * len(keys))
    with get_connection() as conn:
        rows = conn.execute(
            f"SELECT article_url, video_url FROM article_related_video WHERE article_url IN ({placeholders})",
            keys,
        ).fetchall()
    return {row["article_url"]: row["video_url"] for row in rows}


def get_stories(limit: int = 500) -> list[dict[str, Any]]:
    """Return newest stories first for API rendering."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                s.source,
                s.title,
                s.display_title,
                s.url,
                s.summary,
                s.published_at,
                s.place,
                s.country,
                s.lat,
                s.lon,
                c.capital AS fact_capital,
                c.population AS fact_population,
                c.gdp_ppp AS fact_gdp_ppp,
                c.area_total AS fact_area_total,
                c.government_type AS fact_government_type,
                c.economist_economic_rank AS fact_economist_economic_rank
            FROM stories s
            LEFT JOIN cia_country_facts c
                ON lower(c.country_name) = lower(s.country)
            WHERE s.country IS NOT NULL AND s.country != ''
            ORDER BY published_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    stories: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["title"] = (item.get("display_title") or item.get("title") or "").strip()
        item.pop("display_title", None)
        facts = {
            "capital": item.pop("fact_capital"),
            "population": item.pop("fact_population"),
            "gdp_ppp": item.pop("fact_gdp_ppp"),
            "area_total": item.pop("fact_area_total"),
            "government_type": item.pop("fact_government_type"),
            "economist_economic_rank": item.pop("fact_economist_economic_rank"),
        }
        if any(facts.values()):
            item["country_facts"] = facts
        else:
            item["country_facts"] = None
        stories.append(item)

    # Attach verified related video when a social post links to this article.
    urls = list({s["url"] for s in stories})
    related = get_related_video_urls_batch(urls)
    for s in stories:
        s["related_video_url"] = related.get(_normalize_article_url(s["url"])) or None

    return stories


def get_cached_geocode(place: str) -> tuple[float, float, str | None] | None:
    """Read geocode cache by place string."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT lat, lon, country FROM geocode_cache WHERE place = ?",
            (place,),
        ).fetchone()
    if row is None:
        return None
    return float(row["lat"]), float(row["lon"]), row["country"]


def set_cached_geocode(place: str, lat: float, lon: float, country: str | None) -> None:
    """Store geocode cache entry, replacing older value if needed."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO geocode_cache (place, lat, lon, country, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(place) DO UPDATE SET
                lat = excluded.lat,
                lon = excluded.lon,
                country = excluded.country,
                updated_at = excluded.updated_at
            """,
            (place, lat, lon, country, _utc_now_iso()),
        )
        conn.commit()


def upsert_country_fact(fact: dict[str, str | None]) -> None:
    """Insert or update CIA fact fields for one country."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO cia_country_facts (
                country_name, capital, population, gdp_ppp, area_total, government_type,
                economist_economic_rank, cia_risk_rating, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(country_name) DO UPDATE SET
                capital = excluded.capital,
                population = excluded.population,
                gdp_ppp = excluded.gdp_ppp,
                area_total = excluded.area_total,
                government_type = excluded.government_type,
                economist_economic_rank = excluded.economist_economic_rank,
                cia_risk_rating = excluded.cia_risk_rating,
                updated_at = excluded.updated_at
            """,
            (
                fact.get("country_name"),
                fact.get("capital"),
                fact.get("population"),
                fact.get("gdp_ppp"),
                fact.get("area_total"),
                fact.get("government_type"),
                fact.get("economist_economic_rank"),
                fact.get("cia_risk_rating"),
                _utc_now_iso(),
            ),
        )
        conn.commit()


def upsert_country_name(english_name: str, original_name: str) -> None:
    """Store original-language and English labels for a country."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO country_names (english_name, original_name, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(english_name) DO UPDATE SET
                original_name = excluded.original_name,
                updated_at = excluded.updated_at
            """,
            (english_name, original_name, _utc_now_iso()),
        )
        conn.commit()


def upsert_rankings(
    rows: list[tuple[str, str, int | None, float | None, str | None]],
) -> None:
    """Insert or update Economist-style rankings. Each row: (country_name, indicator_key, rank, score, year)."""
    now = _utc_now_iso()
    with get_connection() as conn:
        for country_name, indicator_key, rank_value, score_value, year in rows:
            conn.execute(
                """
                INSERT INTO economist_rankings (
                    country_name, indicator_key, rank_value, score_value, year, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(country_name, indicator_key) DO UPDATE SET
                    rank_value = excluded.rank_value,
                    score_value = excluded.score_value,
                    year = excluded.year,
                    updated_at = excluded.updated_at
                """,
                (country_name, indicator_key, rank_value, score_value, year, now),
            )
        conn.commit()


def get_rankings_for_country(normalized_country_name: str) -> list[dict[str, Any]]:
    """Return list of { indicator_key, label, rank, score, year } for the country."""
    from app.economist_rankings import RANKING_INDICATORS
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT indicator_key, rank_value, score_value, year
            FROM economist_rankings
            WHERE country_name = ?
            ORDER BY indicator_key
            """,
            (normalized_country_name,),
        ).fetchall()
    out = []
    for r in rows:
        out.append({
            "indicator_key": r["indicator_key"],
            "label": RANKING_INDICATORS.get(r["indicator_key"], r["indicator_key"]),
            "rank": r["rank_value"],
            "score": r["score_value"],
            "year": r["year"],
        })
    return out


def _parse_published_ts(published_at: str | None) -> float:
    """Parse published_at to a timestamp for recency tiebreaker; older = smaller."""
    if not published_at:
        return 0.0
    s = (published_at or "").strip()
    try:
        if "T" in s and "-" in s:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        else:
            dt = parsedate_to_datetime(s)
        return dt.timestamp() if dt.tzinfo else dt.replace(tzinfo=timezone.utc).timestamp()
    except Exception:
        return 0.0


def _story_rank_score(
    story: dict[str, Any],
    country_name: str,
    country_pattern: re.Pattern[str],
) -> tuple[int, float]:
    """
    Return (relevance_plus_popularity, -timestamp) for sorting.
    Higher relevance/popularity first; then newer first (negative timestamp so newer = larger).
    """
    title = (story.get("title") or "").strip()
    summary = (story.get("summary") or "").strip()
    blob = f"{title} {summary}"
    relevance = 0
    if country_pattern.search(title):
        relevance += 3
    if country_pattern.search(summary):
        relevance += 1
    if not relevance and country_pattern.search(blob):
        relevance = 1
    source = str(story.get("source") or "").lower()
    popularity = 2 if source in POPULAR_SOURCES else 0
    ts = _parse_published_ts(story.get("published_at"))
    return (relevance + popularity, ts)


def get_country_detail(country_name: str) -> dict[str, Any]:
    """Return CIA facts and relevant recent stories for a selected country."""
    normalized = normalize_country_name(country_name)
    with get_connection() as conn:
        fact_row = conn.execute(
            """
            SELECT country_name, capital, population, gdp_ppp, area_total, government_type,
                   economist_economic_rank, cia_risk_rating
            FROM cia_country_facts
            """,
        ).fetchall()
        matched_fact = None
        for row in fact_row:
            if normalize_country_name(row["country_name"]) == normalized:
                matched_fact = dict(row)
                break
        labels_rows = conn.execute(
            "SELECT english_name, original_name FROM country_names"
        ).fetchall()
        label = None
        for row in labels_rows:
            if normalize_country_name(row["english_name"]) == normalized:
                label = dict(row)
                break

        stories_rows = conn.execute(
            """
            SELECT source, title, display_title, url, summary, published_at, country
            FROM stories
            ORDER BY published_at DESC
            LIMIT 300
            """
        ).fetchall()

    stories = [dict(r) for r in stories_rows]
    for s in stories:
        s["title"] = (s.get("display_title") or s.get("title") or "").strip()
        s.pop("display_title", None)
    stories = [
        s for s in stories if normalize_country_name(s.get("country") or "") == normalized
    ]
    for s in stories:
        s.pop("country", None)
    country_pattern = re.compile(rf"\b{re.escape(country_name)}\b", re.IGNORECASE)

    def rank_key(s: dict[str, Any]) -> tuple[int, float]:
        score, ts = _story_rank_score(s, country_name, country_pattern)
        return (-score, -ts)  # higher score first, then newer first

    all_source_stories = []
    for s in stories:
        blob = f"{s.get('title','')} {s.get('summary','')}"
        if country_pattern.search(blob):
            all_source_stories.append(s)
    if not all_source_stories:
        all_source_stories = list(stories)
    all_source_stories.sort(key=rank_key)
    graphic_detail_stories = [
        s for s in all_source_stories
        if str(s.get("source", "")).lower() == "economist_graphic_detail"
    ][:8]
    all_source_stories = [
        s for s in all_source_stories
        if str(s.get("source", "")).lower() != "economist_graphic_detail"
    ][:40]

    stories.sort(key=rank_key)
    recent_stories = stories[:20]

    source_counts: dict[str, int] = {}
    for s in all_source_stories:
        source = str(s.get("source", "unknown"))
        source_counts[source] = source_counts.get(source, 0) + 1
    if matched_fact:
        matched_fact.pop("cia_risk_rating", None)
    economist_rankings = get_rankings_for_country(normalized)
    return {
        "country_name": matched_fact.get("country_name") if matched_fact else country_name,
        "english_name": (label or {}).get("english_name", country_name),
        "original_name": (label or {}).get("original_name", country_name),
        "facts": matched_fact,
        "economist_rankings": economist_rankings,
        "graphic_detail_stories": graphic_detail_stories,
        "all_source_stories": all_source_stories,
        "source_counts": source_counts,
        "recent_stories": recent_stories,
    }

