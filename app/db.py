"""SQLite helpers for stories and geocode cache."""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from typing import Any


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
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def upsert_story(story: dict[str, Any]) -> None:
    """Insert or update a story by URL so refreshed ingest can improve locations."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO stories (
                source, title, url, summary, published_at, place, lat, lon, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                source = excluded.source,
                title = excluded.title,
                summary = excluded.summary,
                published_at = excluded.published_at,
                place = excluded.place,
                lat = excluded.lat,
                lon = excluded.lon
            """,
            (
                story["source"],
                story["title"],
                story["url"],
                story["summary"],
                story["published_at"],
                story.get("place"),
                story["lat"],
                story["lon"],
                _utc_now_iso(),
            ),
        )
        conn.commit()


def get_stories(limit: int = 500) -> list[dict[str, Any]]:
    """Return newest stories first for API rendering."""
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT source, title, url, summary, published_at, place, lat, lon
            FROM stories
            ORDER BY published_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def get_cached_geocode(place: str) -> tuple[float, float] | None:
    """Read geocode cache by place string."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT lat, lon FROM geocode_cache WHERE place = ?",
            (place,),
        ).fetchone()
    if row is None:
        return None
    return float(row["lat"]), float(row["lon"])


def set_cached_geocode(place: str, lat: float, lon: float) -> None:
    """Store geocode cache entry, replacing older value if needed."""
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO geocode_cache (place, lat, lon, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(place) DO UPDATE SET
                lat = excluded.lat,
                lon = excluded.lon,
                updated_at = excluded.updated_at
            """,
            (place, lat, lon, _utc_now_iso()),
        )
        conn.commit()

