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
from app.conflict_data import CONFLICT_CASUALTIES, COUNTRY_TOP_LEAGUES

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
    "x_rudaw", "x_middleeasteye", "x_kurdistan24", "x_visegrad24",
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
        if not _has_column(conn, "stories", "topic"):
            conn.execute("ALTER TABLE stories ADD COLUMN topic TEXT NULL")
        if not _has_column(conn, "stories", "sport"):
            conn.execute("ALTER TABLE stories ADD COLUMN sport TEXT NULL")
        if not _has_column(conn, "stories", "league"):
            conn.execute("ALTER TABLE stories ADD COLUMN league TEXT NULL")
        if not _has_column(conn, "stories", "team_home"):
            conn.execute("ALTER TABLE stories ADD COLUMN team_home TEXT NULL")
        if not _has_column(conn, "stories", "team_away"):
            conn.execute("ALTER TABLE stories ADD COLUMN team_away TEXT NULL")
        if not _has_column(conn, "stories", "location_type"):
            conn.execute("ALTER TABLE stories ADD COLUMN location_type TEXT NULL")
        if not _has_column(conn, "stories", "city"):
            conn.execute("ALTER TABLE stories ADD COLUMN city TEXT NULL")
        if not _has_column(conn, "stories", "country_code"):
            conn.execute("ALTER TABLE stories ADD COLUMN country_code TEXT NULL")
        _migrate_stories_nullable_lat_lon(conn)
        if not _has_column(conn, "stories", "pvd_score"):
            conn.execute("ALTER TABLE stories ADD COLUMN pvd_score REAL NULL")
        if not _has_column(conn, "stories", "content_type"):
            conn.execute("ALTER TABLE stories ADD COLUMN content_type TEXT NULL")
        conn.commit()


def _has_column(conn: sqlite3.Connection, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(row["name"] == column for row in rows)


def _migrate_stories_nullable_lat_lon(conn: sqlite3.Connection) -> None:
    """Recreate stories so lat/lon can be NULL (country-only stories). Run after location_type/city/country_code exist."""
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='stories'"
    ).fetchone()
    if not row or not row[0]:
        return
    if "lat REAL NULL" in row[0].replace("  ", " "):
        return
    conn.execute(
        """
        CREATE TABLE stories_nullable_lat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            summary TEXT NOT NULL,
            published_at TEXT NOT NULL,
            place TEXT NULL,
            lat REAL NULL,
            lon REAL NULL,
            created_at TEXT NOT NULL,
            country TEXT NULL,
            display_title TEXT NULL,
            topic TEXT NULL,
            sport TEXT NULL,
            league TEXT NULL,
            team_home TEXT NULL,
            team_away TEXT NULL,
            location_type TEXT NULL,
            city TEXT NULL,
            country_code TEXT NULL,
            UNIQUE(url, country)
        )
        """
    )
    conn.execute(
        """
        INSERT INTO stories_nullable_lat (
            id, source, title, url, summary, published_at, place, lat, lon, created_at,
            country, display_title, topic, sport, league, team_home, team_away,
            location_type, city, country_code
        )
        SELECT
            id, source, title, url, summary, published_at, place, lat, lon, created_at,
            country, display_title, topic, sport, league, team_home, team_away,
            location_type, city, country_code
        FROM stories
        """
    )
    conn.execute("DROP TABLE stories")
    conn.execute("ALTER TABLE stories_nullable_lat RENAME TO stories")


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
    """Insert or update a story by (URL, country). Supports country-only stories (lat/lon NULL)."""
    country = story.get("country") or ""
    display_title = (story.get("display_title") or "").strip() or None
    topic = (story.get("topic") or "").strip() or None
    sport = (story.get("sport") or "").strip() or None
    league = (story.get("league") or "").strip() or None
    team_home = (story.get("team_home") or "").strip() or None
    team_away = (story.get("team_away") or "").strip() or None
    location_type = (story.get("location_type") or "").strip() or None
    city = (story.get("city") or "").strip() or None
    country_code = (story.get("country_code") or "").strip() or None
    content_type = (story.get("content_type") or "").strip() or None
    pvd_score = story.get("pvd_score")
    if pvd_score is not None and not isinstance(pvd_score, (int, float)):
        pvd_score = None
    lat = story.get("lat")
    lon = story.get("lon")
    if lat is not None and not isinstance(lat, (int, float)):
        lat = None
    if lon is not None and not isinstance(lon, (int, float)):
        lon = None
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO stories (
                source, title, url, summary, published_at, place, country, lat, lon, created_at,
                display_title, topic, sport, league, team_home, team_away,
                location_type, city, country_code, pvd_score, content_type
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url, country) DO UPDATE SET
                source = excluded.source,
                title = excluded.title,
                summary = excluded.summary,
                published_at = excluded.published_at,
                place = excluded.place,
                lat = excluded.lat,
                lon = excluded.lon,
                display_title = COALESCE(excluded.display_title, stories.display_title),
                topic = COALESCE(excluded.topic, stories.topic),
                sport = COALESCE(excluded.sport, stories.sport),
                league = COALESCE(excluded.league, stories.league),
                team_home = COALESCE(excluded.team_home, stories.team_home),
                team_away = COALESCE(excluded.team_away, stories.team_away),
                location_type = COALESCE(excluded.location_type, stories.location_type),
                city = COALESCE(excluded.city, stories.city),
                country_code = COALESCE(excluded.country_code, stories.country_code),
                pvd_score = COALESCE(excluded.pvd_score, stories.pvd_score),
                content_type = COALESCE(excluded.content_type, stories.content_type)
            """,
            (
                story["source"],
                story["title"],
                story["url"],
                story["summary"],
                story["published_at"],
                story.get("place"),
                country,
                lat,
                lon,
                _utc_now_iso(),
                display_title,
                topic,
                sport,
                league,
                team_home,
                team_away,
                location_type,
                city,
                country_code,
                pvd_score,
                content_type,
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


def _apply_time_relevance_filter(
    stories: list[dict[str, Any]], limit: int
) -> list[dict[str, Any]]:
    """
    Filter stories by time-based relevance: older stories drop off.
    Regions with fewer recent stories keep stories longer (extended retention).
    """
    # Add days_ago for each story
    for s in stories:
        s["_days_ago"] = _published_days_ago(s.get("published_at"))

    # Count how many stories per (normalized) country are in the recent window
    recent_count: dict[str, int] = {}
    for s in stories:
        days = s.get("_days_ago")
        if days is None:
            continue
        country = normalize_country_name((s.get("country") or "").strip())
        if not country or country == "World":
            continue
        if days <= RECENT_WINDOW_DAYS:
            recent_count[country] = recent_count.get(country, 0) + 1

    # Max age per country: more recent stories -> shorter window; fewer -> longer
    max_age_days: dict[str, int] = {}
    for country, count in recent_count.items():
        if count >= RECENT_HIGH_THRESHOLD:
            max_age_days[country] = MAX_AGE_DAYS_DEFAULT
        elif count <= RECENT_LOW_THRESHOLD:
            max_age_days[country] = MAX_AGE_DAYS_EXTENDED
        else:
            max_age_days[country] = 14  # between 7 and 30

    # Keep story if within its country's max age. Unknown/sparse regions (not in max_age_days) get extended retention.
    filtered: list[dict[str, Any]] = []
    for s in stories:
        days = s.get("_days_ago")
        country = normalize_country_name((s.get("country") or "").strip())
        if not country or country == "World":
            country = "World"
        # Sparse or no recent stories -> keep longer (default extended); else use computed max_age
        max_age = max_age_days.get(country, MAX_AGE_DAYS_EXTENDED)
        if days is None:
            filtered.append(s)  # unparseable date: keep
        elif days <= max_age:
            filtered.append(s)
        s.pop("_days_ago", None)

    # Sort by published_at desc (newest first), take limit
    filtered.sort(
        key=lambda x: _parse_published_ts(x.get("published_at")),
        reverse=True,
    )
    return filtered[:limit]


def get_stories(limit: int = 500, year: int | None = None) -> list[dict[str, Any]]:
    """Return newest stories first for API rendering. If year is set, only stories from that year (AD).
    For BC years (year < 1) the DB has no rows; use historical events API instead.
    When year is None, stories are filtered by time relevance: they age out, with longer retention
    in regions that have fewer recent stories."""
    if year is not None and year < 1:
        return []
    # When showing "current" map, fetch more rows so we can apply time/region-aware filtering
    fetch_limit = limit * 4 if year is None else limit
    with get_connection() as conn:
        if year is not None:
            sql = """
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
                s.topic,
                s.sport,
                s.league,
                s.team_home,
                s.team_away,
                s.location_type,
                s.city,
                s.country_code,
                s.pvd_score,
                s.content_type,
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
            AND strftime('%Y', s.published_at) = ?
            ORDER BY published_at DESC
            LIMIT ?
            """
            rows = conn.execute(sql, (str(year), limit)).fetchall()
        else:
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
                    s.topic,
                    s.sport,
                    s.league,
                    s.team_home,
                    s.team_away,
                    s.location_type,
                    s.city,
                    s.country_code,
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
                (fetch_limit,),
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

    if year is None:
        stories = _apply_time_relevance_filter(stories, limit)

    # Attach verified related video when a social post links to this article.
    urls = list({s["url"] for s in stories})
    related = get_related_video_urls_batch(urls)
    for s in stories:
        s["related_video_url"] = related.get(_normalize_article_url(s["url"])) or None

    return stories


def get_story_count_by_country() -> dict[str, int]:
    """Return normalized country name -> number of stories (excludes World). For ingest prioritization."""
    from app.factbook import normalize_country_name
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT country, COUNT(*) AS cnt FROM stories
            WHERE country IS NOT NULL AND country != '' AND country != 'World'
            GROUP BY country
            """
        ).fetchall()
    counts: dict[str, int] = {}
    for row in rows:
        norm = normalize_country_name(row["country"] or "")
        if norm:
            counts[norm] = counts.get(norm, 0) + row["cnt"]
    return counts


def get_total_mapped_story_count() -> int:
    """Total number of stories pinned to a country (excludes World)."""
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT COUNT(*) AS n FROM stories
            WHERE country IS NOT NULL AND country != '' AND country != 'World'
            """
        ).fetchone()
    return row["n"] if row else 0


def get_all_countries_baseline() -> list[dict[str, Any]]:
    """
    Return baseline info for every country in the CIA factbook (for chatbot context).
    Ensures the bot can answer questions about any country even when there are no recent stories.
    """
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT country_name, capital, population, gdp_ppp, area_total, government_type
            FROM cia_country_facts
            ORDER BY country_name
            """
        ).fetchall()
    return [dict(r) for r in rows]


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


def _published_days_ago(published_at: str | None) -> float | None:
    """Return days since published, or None if unparseable."""
    ts = _parse_published_ts(published_at)
    if ts <= 0:
        return None
    delta = datetime.now(timezone.utc).timestamp() - ts
    return delta / (24 * 3600)


# Time-based relevance: stories age out; sparse regions keep stories longer.
# If a country has many recent stories (>= RECENT_HIGH), use short window; else extend.
RECENT_WINDOW_DAYS = 7
MAX_AGE_DAYS_DEFAULT = 7
MAX_AGE_DAYS_EXTENDED = 30
RECENT_HIGH_THRESHOLD = 10  # >= this many in last 7 days -> 7-day max age
RECENT_LOW_THRESHOLD = 3   # <= this many -> 30-day max age; between -> 14 days


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


def get_country_detail(country_name: str, year: int | None = None) -> dict[str, Any]:
    """Return CIA facts and relevant recent stories for a selected country.
    If year is set, only include stories with published_at year <= year (for historical border view)."""
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
            SELECT source, title, display_title, url, summary, published_at, country, topic,
                   lat, lon, location_type, city, country_code, pvd_score, content_type
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
    if year is not None:
        def _story_year(s: dict[str, Any]) -> int | None:
            ts = s.get("published_at")
            if not ts:
                return None
            try:
                return int(str(ts)[:4])
            except (ValueError, TypeError):
                return None
        stories = [s for s in stories if (_story_year(s) or 0) <= year]
    for s in stories:
        s.pop("country", None)

    # Merge seed/fill from data/country_news so every country has at least one item.
    try:
        from app.country_news import get_country_news, get_placeholder_story
        from app.geo.location import _country_name_to_iso2
        iso2 = _country_name_to_iso2(country_name)
        if not iso2 and stories:
            iso2 = (stories[0].get("country_code") or "").strip() or None
        seed_items = get_country_news(country_name)
        for item in seed_items:
            if not any(
                s.get("url") == item.get("url") and s.get("title") == item.get("title")
                for s in stories
            ):
                stories.append(item)
        if not stories:
            stories.append(get_placeholder_story(country_name, iso2))
    except Exception:
        if not stories:
            try:
                from app.country_news import get_placeholder_story
                from app.geo.location import _country_name_to_iso2
                iso2 = _country_name_to_iso2(country_name)
                stories.append(get_placeholder_story(country_name, iso2))
            except Exception:
                pass

    try:
        from app.ranking import score_story_pvd
        for s in stories:
            if s.get("pvd_score") is None:
                s["pvd_score"] = score_story_pvd(s)
    except Exception:
        pass
    country_pattern = re.compile(rf"\b{re.escape(country_name)}\b", re.IGNORECASE)

    def pvd_sort_key(s: dict[str, Any]) -> tuple[float, float]:
        pvd = float(s.get("pvd_score") or 0.0)
        ts = _parse_published_ts(s.get("published_at"))
        return (-pvd, -ts)  # higher PVD score first, then newer first

    all_source_stories = []
    for s in stories:
        blob = f"{s.get('title','')} {s.get('summary','')}"
        if country_pattern.search(blob):
            all_source_stories.append(s)
    if not all_source_stories:
        all_source_stories = list(stories)
    all_source_stories.sort(key=pvd_sort_key)
    graphic_detail_stories = [
        s for s in all_source_stories
        if str(s.get("source", "")).lower() == "economist_graphic_detail"
    ][:8]
    all_source_stories = [
        s for s in all_source_stories
        if str(s.get("source", "")).lower() != "economist_graphic_detail"
    ][:40]

    stories.sort(key=pvd_sort_key)
    recent_stories = stories[:20]

    source_counts: dict[str, int] = {}
    for s in all_source_stories:
        source = str(s.get("source", "unknown"))
        source_counts[source] = source_counts.get(source, 0) + 1
    if matched_fact:
        matched_fact.pop("cia_risk_rating", None)
    economist_rankings = get_rankings_for_country(normalized)
    conflict_casualties = CONFLICT_CASUALTIES.get(normalized)
    top_sports_leagues = COUNTRY_TOP_LEAGUES.get(normalized)
    wikipedia_snippet = None
    try:
        from app.historical_events import UNDER_REPORTED_NORMALIZED, fetch_wikipedia_country_snippet
        if normalized and normalized.lower() in UNDER_REPORTED_NORMALIZED:
            display_name = (label or {}).get("english_name", country_name) or country_name
            wikipedia_snippet = fetch_wikipedia_country_snippet(display_name)
    except Exception:
        pass
    # Economic snapshot from free sources (World Bank, IMF WEO, OECD). Replaces Economist/paywalled macro data.
    econ_snapshot = {}
    try:
        from app.econ.snapshot import get_country_econ_snapshot
        display_name = (label or {}).get("english_name", country_name) or matched_fact.get("country_name") or country_name
        econ_snapshot = get_country_econ_snapshot(None, display_name)
    except Exception:
        pass
    return {
        "country_name": matched_fact.get("country_name") if matched_fact else country_name,
        "english_name": (label or {}).get("english_name", country_name),
        "original_name": (label or {}).get("original_name", country_name),
        "facts": matched_fact,
        "economist_rankings": economist_rankings,
        "econ_snapshot": econ_snapshot,
        "graphic_detail_stories": graphic_detail_stories,
        "all_source_stories": all_source_stories,
        "source_counts": source_counts,
        "recent_stories": recent_stories,
        "conflict_casualties": conflict_casualties,
        "top_sports_leagues": top_sports_leagues or [],
        "wikipedia_snippet": wikipedia_snippet,
    }

