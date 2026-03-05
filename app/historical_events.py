"""
Fetch historical events by year from Wikipedia for the time-travel map view.
Returns story-like dicts (title, summary, country, lat, lon, published_at, source) for years back to 1000 BC.

Use: Map data only (pins on the map). This module does not feed into AI-generated summaries;
those are produced by the model from its own knowledge and context, not from Wikipedia text.
"""

from __future__ import annotations

import logging
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

log = logging.getLogger(__name__)

WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_USER_AGENT = "pvdmaproom/1.0 (historical map; contact via GitHub)"

# Normalized (lowercase) country names where Wikipedia may be used to inform map data (under-reported regions).
UNDER_REPORTED_NORMALIZED = frozenset({
    "algeria", "angola", "benin", "burkina faso", "burundi", "cameroon", "central african republic",
    "chad", "democratic republic of the congo", "djibouti", "eritrea", "ethiopia", "gabon", "gambia",
    "ghana", "guinea", "guinea-bissau", "ivory coast", "kenya", "lesotho", "liberia", "libya",
    "madagascar", "malawi", "mali", "mauritania", "mozambique", "niger", "nigeria", "rwanda",
    "senegal", "sierra leone", "somalia", "south sudan", "sudan", "tanzania", "togo", "tunisia",
    "uganda", "zambia", "zimbabwe", "myanmar", "laos", "cambodia", "brunei", "east timor", "papua new guinea",
    "yemen", "jordan", "lebanon", "syria", "iraq", "afghanistan", "tajikistan", "kyrgyzstan", "turkmenistan",
    "mongolia", "nepal", "bhutan", "sri lanka", "bangladesh", "haiti", "bolivia", "paraguay", "suriname",
    "guyana", "belize", "nicaragua", "honduras", "el salvador", "guatemala", "cuba", "dominican republic",
})

# Country names and common variants for matching in event text (lowercase).
_COUNTRY_TERMS = (
    "afghanistan", "albania", "algeria", "argentina", "australia", "austria", "belgium", "brazil",
    "bulgaria", "cambodia", "canada", "chile", "china", "colombia", "cuba", "czech", "egypt",
    "ethiopia", "finland", "france", "germany", "greece", "hungary", "india", "indonesia", "iran",
    "iraq", "ireland", "israel", "italy", "japan", "kenya", "korea", "libya", "malaysia", "mexico",
    "mongolia", "myanmar", "netherlands", "nigeria", "norway", "pakistan", "peru", "philippines",
    "poland", "romania", "russia", "south africa", "spain", "sudan", "syria", "taiwan", "thailand",
    "turkey", "ukraine", "united kingdom", "united states", "usa", "ussr", "soviet union", "vietnam",
    "yemen", "zimbabwe", "england", "scotland", "wales", "iran", "palestine", "israel",
)


def _wiki_request(params: dict[str, str]) -> dict[str, Any] | None:
    url = WIKI_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": WIKI_USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            import json
            return json.loads(resp.read().decode())
    except (urllib.error.URLError, OSError, ValueError) as e:
        log.warning("Wikipedia request failed: %s", e)
        return None


def _extract_events_from_html(html: str) -> list[str]:
    """Extract event bullet lines from parsed Wikipedia HTML (Events section)."""
    events: list[str] = []
    # Find Events section (h2 or h3); then capture content until next same-level heading.
    event_section = re.search(
        r"<h[23][^>]*>[\s]*Events[\s]*</h[23]>.*?(?=<h[23]|$)",
        html,
        re.IGNORECASE | re.DOTALL,
    )
    if not event_section:
        return events
    block = event_section.group(0)
    # Strip tags and get lines that look like bullets or numbered items.
    block = re.sub(r"<[^>]+>", " ", block)
    block = re.sub(r"&[#\w]+;", " ", block)
    for line in block.split("\n"):
        line = line.strip()
        if not line or len(line) < 15:
            continue
        # Remove leading * or # or "January 1 –" style
        line = re.sub(r"^[\*#\-\d]+\s*", "", line)
        line = re.sub(r"^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+\s*[–\-]\s*", "", line, flags=re.IGNORECASE)
        if len(line) > 20:
            events.append(line[:600])
    return events[:80]


def _find_country_in_text(text: str) -> str | None:
    """Return first matching country (or variant) from text, for geocoding."""
    lower = text.lower()
    for term in _COUNTRY_TERMS:
        if term in lower:
            # Map variants to canonical name for geocoding
            if term in ("usa", "united states"):
                return "United States"
            if term in ("uk", "england", "scotland", "wales", "united kingdom"):
                return "United Kingdom"
            if term in ("ussr", "soviet union"):
                return "Russia"
            if term in ("korea",):
                return "South Korea"  # default for 20th c.
            return term.title()
    return None


def _geocode_place(place: str) -> tuple[float, float] | None:
    """Return (lat, lon) for a place name using app geocoder if available."""
    try:
        from app.db import get_cached_geocode
        from app.db import set_cached_geocode
        from app.factbook import normalize_country_name
        from geopy.geocoders import Nominatim
        cached = get_cached_geocode(place)
        if cached:
            return (cached[0], cached[1])
        geocoder = Nominatim(user_agent=WIKI_USER_AGENT)
        result = geocoder.geocode(place, timeout=3)
        if result:
            lat, lon = float(result.latitude), float(result.longitude)
            country = result.raw.get("address", {}).get("country") if isinstance(result.raw, dict) else None
            set_cached_geocode(place, lat, lon, country)
            return (lat, lon)
    except Exception:
        pass
    return None


def fetch_historical_events(year: int) -> list[dict[str, Any]]:
    """
    Return a list of story-like dicts for the given year.
    year: AD year (e.g. 1979) or negative for BC (e.g. -1000 for 1000 BC).
    """
    if year > 2030 or year < -1000:
        return []
    if year < 1:
        page_title = f"{abs(year)}_BC"
        year_label = f"{abs(year)} BC"
    else:
        page_title = str(year)
        year_label = str(year)

    params = {
        "action": "parse",
        "page": page_title,
        "prop": "text",
        "format": "json",
        "origin": "*",
    }
    data = _wiki_request(params)
    if not data or "parse" not in data or "text" not in data.get("parse", {}):
        # Fallback: try "Events of YYYY" for AD
        if year >= 1:
            params["page"] = f"Events_of_{year}"
            data = _wiki_request(params)
        if not data or "parse" not in data:
            return _fallback_year_summary(year, year_label)

    text_node = data.get("parse", {}).get("text")
    if isinstance(text_node, dict):
        html = text_node.get("*", "")
    else:
        html = text_node or ""
    events = _extract_events_from_html(html)
    if not events:
        return _fallback_year_summary(year, year_label)

    results: list[dict[str, Any]] = []
    seen_countries: set[str] = set()
    default_lat, default_lon = 20.0, 0.0  # fallback

    for ev in events:
        country = _find_country_in_text(ev)
        if country and country not in seen_countries:
            coords = _geocode_place(country)
            if coords:
                lat, lon = coords
                seen_countries.add(country)
            else:
                lat, lon = default_lat, default_lon
        else:
            if not country:
                country = "World"
            lat, lon = default_lat, default_lon
        title = ev[:120] + ("..." if len(ev) > 120 else "")
        results.append({
            "source": "wikipedia_historical",
            "title": title,
            "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(page_title)}",
            "summary": ev[:500],
            "published_at": f"{year_label}-01-01T00:00:00Z" if year >= 1 else f"{abs(year)}-01-01 BC",
            "place": country,
            "country": country,
            "lat": lat,
            "lon": lon,
        })
    return results[:100]


def _fallback_year_summary(year: int, year_label: str) -> list[dict[str, Any]]:
    """When the year page has no events section, return one world-level summary."""
    # Try summary API for a short extract
    if year >= 1:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{year}"
    else:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{abs(year)}_BC"
    req = urllib.request.Request(url, headers={"User-Agent": WIKI_USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            import json
            data = json.loads(resp.read().decode())
        ext = (data.get("extract") or data.get("extract_html") or "")[:800]
        if isinstance(ext, str) and ext:
            title = f"Events in {year_label}"
            page_slug = f"{year}" if year >= 1 else f"{abs(year)}_BC"
            return [{
                "source": "wikipedia_historical",
                "title": title,
                "url": f"https://en.wikipedia.org/wiki/{page_slug}",
                "summary": ext,
                "published_at": f"{year_label}-01-01T00:00:00Z",
                "place": "World",
                "country": "World",
                "lat": 20.0,
                "lon": 0.0,
            }]
    except Exception:
        pass
    return [{
        "source": "wikipedia_historical",
        "title": f"Year {year_label}",
        "url": "https://en.wikipedia.org/wiki/History_of_the_world",
        "summary": f"Historical events in {year_label}. Select a country for an AI-generated summary focused on that year.",
        "published_at": f"{year_label}-01-01T00:00:00Z",
        "place": "World",
        "country": "World",
        "lat": 20.0,
        "lon": 0.0,
    }]


def fetch_wikipedia_country_snippet(country_name: str) -> str | None:
    """
    Fetch a short Wikipedia extract for a country (map data only).
    Used only for under-reported countries to add context. Not for AI summaries.
    Returns 1-2 sentences or None on failure.
    """
    if not (country_name or "").strip():
        return None
    title = (country_name or "").strip()
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + urllib.parse.quote(title.replace(" ", "_"))
    req = urllib.request.Request(url, headers={"User-Agent": WIKI_USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            import json
            data = json.loads(resp.read().decode())
        ext = (data.get("extract") or "").strip()
        if ext:
            return ext[:400].rsplit(".", 1)[0] + "." if "." in ext[:400] else ext[:400]
    except Exception:
        pass
    return None
