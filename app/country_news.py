"""
Country news abstraction: seed data and placeholder so every country has at least one item.

Data pipeline: news comes from (1) DB stories from ingest, (2) seed JSON in data/country_news/.
get_country_news(country_name) returns story-like items keyed by country (ISO2) for merging
into get_country_detail. Edit data/country_news/seed.json by hand or use scripts/seed_country_news.py.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SEED_CACHE: dict[str, list[dict[str, Any]]] | None = None
_CENTROIDS_CACHE: dict[str, list[float]] | None = None

def _data_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "country_news"

def _country_name_to_iso2(country_name: str) -> str | None:
    try:
        from app.geo.location import _country_name_to_iso2 as resolve
        return resolve(country_name)
    except Exception:
        return None

def _load_centroids() -> dict[str, list[float]]:
    global _CENTROIDS_CACHE
    if _CENTROIDS_CACHE is not None:
        return _CENTROIDS_CACHE
    path = _data_dir() / "centroids.json"
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as f:
                _CENTROIDS_CACHE = json.load(f)
            return _CENTROIDS_CACHE or {}
        except Exception:
            pass
    _CENTROIDS_CACHE = {}
    return _CENTROIDS_CACHE

def _load_seed() -> dict[str, list[dict[str, Any]]]:
    """Load seed.json; keys are ISO2, values are lists of raw seed items."""
    global _SEED_CACHE
    if _SEED_CACHE is not None:
        return _SEED_CACHE
    path = _data_dir() / "seed.json"
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            # Support both { "US": [...] } and { "countries": { "US": [...] } }
            if isinstance(data, dict) and "countries" in data:
                _SEED_CACHE = data.get("countries") or {}
            else:
                _SEED_CACHE = {k: v for k, v in (data or {}).items() if isinstance(v, list)}
            return _SEED_CACHE or {}
        except Exception:
            pass
    _SEED_CACHE = {}
    return _SEED_CACHE

def _seed_item_to_story(item: dict[str, Any], iso2: str, country_display_name: str) -> dict[str, Any]:
    """Convert a seed entry to a story-like dict for the API/sidebar."""
    lat = item.get("lat")
    lon = item.get("lon")
    centroids = _load_centroids()
    if (lat is None or lon is None) and iso2 in centroids:
        coords = centroids[iso2]
        if isinstance(coords, (list, tuple)) and len(coords) >= 2:
            lat, lon = float(coords[0]), float(coords[1])
    if lat is None:
        lat = 0.0
    if lon is None:
        lon = 0.0
    title = (item.get("title") or "").strip() or "Overview"
    summary = (item.get("summary") or "").strip() or "Key facts and recent context."
    url = (item.get("source_url") or item.get("url") or "").strip() or f"https://en.wikipedia.org/wiki/{country_display_name.replace(' ', '_')}"
    date = (item.get("date") or "").strip() or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if len(date) <= 10:
        date = date + "T12:00:00+00:00"
    elif "T" not in date:
        date = date + "T12:00:00+00:00"
    source = (item.get("source") or "Seed").strip()
    topic = (item.get("topic") or "geopolitics").strip().lower()
    if topic not in ("economics", "geopolitics", "conflicts", "sports"):
        topic = "geopolitics"
    return {
        "title": title,
        "display_title": title,
        "summary": summary,
        "url": url,
        "published_at": date,
        "source": source,
        "lat": float(lat),
        "lon": float(lon),
        "topic": topic,
        "country_code": iso2,
        "location_type": "country",
        "pvd_score": 1.0,
        "content_type": "reporting",
    }

def get_country_news(country_name: str) -> list[dict[str, Any]]:
    """
    Return story-like items for this country from the seed layer.
    Used to fill the sidebar when DB has no stories for this country.
    country_name can be English name or ISO2.
    If the country has no seed entries, returns one generic overview item so the UI always has something to show.
    """
    iso2 = _country_name_to_iso2(country_name)
    if not iso2:
        return []
    seed = _load_seed()
    items = seed.get(iso2.upper()) or seed.get(iso2) or []
    display = (country_name or "").strip() if len((country_name or "").strip()) > 2 else iso2
    if items:
        return [_seed_item_to_story(item, iso2.upper(), display) for item in items]
    # No seed entry for this country: return one generic overview so every country has at least one item
    return [get_placeholder_story(country_name, iso2.upper())]

def get_placeholder_story(country_name: str, iso2: str | None) -> dict[str, Any]:
    """One generic item so the panel is never empty. Used when no seed or DB stories exist for this country."""
    if not iso2:
        iso2 = _country_name_to_iso2(country_name) or "XX"
    centroids = _load_centroids()
    lat, lon = 20.0, 0.0
    if iso2 in centroids and isinstance(centroids[iso2], (list, tuple)) and len(centroids[iso2]) >= 2:
        lat, lon = float(centroids[iso2][0]), float(centroids[iso2][1])
    name = (country_name or iso2).strip()
    wiki_slug = name.replace(" ", "_")
    return {
        "title": f"Overview: {name}",
        "display_title": f"Overview: {name}",
        "summary": "General overview and key facts for this country. Edit data/country_news/seed.json or use Admin → Seed to add real headlines; the ingest pipeline also fetches news when running.",
        "url": f"https://en.wikipedia.org/wiki/{wiki_slug}",
        "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT12:00:00+00:00"),
        "source": "PVD Map",
        "lat": lat,
        "lon": lon,
        "topic": "geopolitics",
        "country_code": iso2,
        "location_type": "country",
        "pvd_score": 0.5,
        "content_type": "reporting",
    }

def invalidate_cache() -> None:
    """Clear in-memory seed/centroid cache (e.g. after admin edits)."""
    global _SEED_CACHE, _CENTROIDS_CACHE
    _SEED_CACHE = None
    _CENTROIDS_CACHE = None
