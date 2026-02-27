"""Ingestion entrypoint: fetch stories, geocode, and store in SQLite."""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

from geopy.exc import GeocoderServiceError, GeopyError
from geopy.geocoders import Nominatim

from app.db import get_cached_geocode, init_db, set_cached_geocode, upsert_story
from app.sources.bbc import fetch_bbc_world
from app.sources.nyt import fetch_nyt_top_stories

# Fallback for stories where we cannot infer a place.
FALLBACK_PLACE = "London"
FALLBACK_COORDS = (51.5074, -0.1278)

# Regex patterns for simple place extraction.
PAREN_PLACE_RE = re.compile(r"\(([A-Z][A-Za-z .'-]{1,60})\)")
IN_PLACE_RE = re.compile(r"\b(?:in|at|near|from)\s+([A-Z][A-Za-z .'-]{1,60})")
LEADING_COLON_RE = re.compile(r"^\s*([A-Z][A-Za-z .'-]{1,60})\s*:")
EVENT_PREFIX_RE = re.compile(
    r"\b([A-Z][A-Za-z .'-]{1,40})\s+"
    r"(?:war|conflict|floods?|earthquake|election|protests?|crisis|offensive)\b"
)


def _normalize_published_at(raw_value: str) -> str:
    """Convert published date string into ISO-8601 UTC."""
    if not raw_value:
        return datetime.now(timezone.utc).isoformat()

    # RSS often uses RFC 2822. Try robust parser first.
    try:
        dt = parsedate_to_datetime(raw_value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError):
        pass

    # If parser fails, keep value as-is to avoid data loss.
    return raw_value


def _extract_place_candidates(text: str) -> list[str]:
    """Extract likely place candidates from text using simple headline patterns."""
    if not text:
        return []

    candidates: list[str] = []

    # Pattern: "(Paris)" or "(Gaza)".
    for match in PAREN_PLACE_RE.finditer(text):
        candidates.append(match.group(1).strip())

    # Pattern: "in X", "at X", "near X", "from X".
    for match in IN_PLACE_RE.finditer(text):
        candidates.append(match.group(1).strip(" .,:;"))

    # Pattern: "Sudan: ...", common in news headlines.
    lead = LEADING_COLON_RE.search(text)
    if lead:
        candidates.append(lead.group(1).strip())

    # Pattern: "Sudan war ...", "Gaza conflict ...", etc.
    for match in EVENT_PREFIX_RE.finditer(text):
        candidates.append(match.group(1).strip())

    # Keep first occurrence order while removing duplicates.
    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = candidate.lower()
        if key in seen:
            continue
        deduped.append(candidate)
        seen.add(key)

    return deduped


def _guess_place_candidates(story: dict[str, Any]) -> list[str]:
    """Gather place candidates from title first, then summary."""
    title = story.get("title", "")
    summary = story.get("summary", "")
    candidates: list[str] = []

    candidates.extend(_extract_place_candidates(title))
    candidates.extend(_extract_place_candidates(summary))

    # Keep first occurrence order while removing duplicates.
    deduped: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = candidate.lower()
        if key in seen:
            continue
        deduped.append(candidate)
        seen.add(key)

    return deduped


def _get_geocoder() -> Nominatim:
    # Use an explicit user agent per Nominatim usage policy.
    return Nominatim(user_agent="pvdmaproom-news-map")


def _geocode_place(
    geocoder: Nominatim, place: str, fallback_to_default: bool
) -> tuple[float, float] | None:
    """Geocode with persistent cache to avoid duplicate requests."""
    cached = get_cached_geocode(place)
    if cached is not None:
        return cached

    try:
        result = geocoder.geocode(place, timeout=10)
    except (GeocoderServiceError, GeopyError):
        result = None

    if result is None:
        if not fallback_to_default:
            return None
        coords = FALLBACK_COORDS
    else:
        coords = (float(result.latitude), float(result.longitude))

    set_cached_geocode(place, coords[0], coords[1])
    return coords


def _resolve_story_location(
    geocoder: Nominatim, story: dict[str, Any]
) -> tuple[str, float, float]:
    """
    Resolve best-effort event location:
    try inferred candidates first, then fallback to London.
    """
    for candidate in _guess_place_candidates(story):
        coords = _geocode_place(geocoder, candidate, fallback_to_default=False)
        if coords is not None:
            return candidate, coords[0], coords[1]

    fallback_coords = _geocode_place(geocoder, FALLBACK_PLACE, fallback_to_default=True)
    if fallback_coords is None:
        # Defensive fallback for unexpected geocoder/cache errors.
        return FALLBACK_PLACE, FALLBACK_COORDS[0], FALLBACK_COORDS[1]
    return FALLBACK_PLACE, fallback_coords[0], fallback_coords[1]


def _sanitize_story(story: dict[str, Any]) -> dict[str, Any] | None:
    """Drop malformed stories so ingestion can continue safely."""
    title = str(story.get("title", "")).strip()
    url = str(story.get("url", "")).strip()
    summary = str(story.get("summary", "")).strip()
    source = str(story.get("source", "")).strip()
    published_at = _normalize_published_at(str(story.get("published_at", "")).strip())

    if not title or not url or not source:
        return None

    return {
        "source": source,
        "title": title,
        "url": url,
        "summary": summary,
        "published_at": published_at,
    }


def run_ingest() -> None:
    """Fetch all enabled sources and insert stories into SQLite."""
    init_db()
    geocoder = _get_geocoder()

    incoming: list[dict[str, Any]] = []
    incoming.extend(fetch_bbc_world())

    nyt_api_key = os.getenv("NYT_API_KEY", "").strip()
    if nyt_api_key:
        incoming.extend(fetch_nyt_top_stories(nyt_api_key))

    for raw_story in incoming:
        story = _sanitize_story(raw_story)
        if story is None:
            continue

        place, lat, lon = _resolve_story_location(geocoder, story)
        story["place"] = place
        story["lat"] = lat
        story["lon"] = lon
        upsert_story(story)


if __name__ == "__main__":
    run_ingest()

