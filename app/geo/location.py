"""
Unified location pipeline: entity extraction (people vs places vs teams),
topic-aware geocoding, and stadium-based location for sports stories.
Entry point: attach_location(story).
"""

from __future__ import annotations

import json
import logging
import re
import time
from typing import Any

from geopy.exc import GeocoderServiceError, GeopyError
from geopy.geocoders import Nominatim

from app.ai_summary import _client
from app.ai_summary import SUMMARY_MODEL
from app.db import get_cached_geocode, set_cached_geocode
from app.geo.stadiums import get_stadium_for_team

log = logging.getLogger(__name__)


def _country_name_to_iso2(country_name: str) -> str | None:
    """Resolve country name to ISO 3166-1 alpha-2 (e.g. US, DE). Returns None if not found."""
    if not (country_name and isinstance(country_name, str)):
        return None
    s = country_name.strip()
    if len(s) == 2 and s.isalpha():
        return s.upper()
    key = s.lower().replace(",", "").strip()
    _common: dict[str, str] = {
        "united states": "US", "united states of america": "US", "usa": "US",
        "united kingdom": "GB", "great britain": "GB", "uk": "GB",
        "germany": "DE", "france": "FR", "japan": "JP", "china": "CN",
        "brazil": "BR", "india": "IN", "canada": "CA", "australia": "AU",
        "russia": "RU", "italy": "IT", "spain": "ES", "south korea": "KR",
        "mexico": "MX", "indonesia": "ID", "netherlands": "NL", "turkey": "TR",
    }
    if key in _common:
        return _common[key]
    try:
        import pycountry
        c = pycountry.countries.get(name=s)
        if not c:
            matches = pycountry.countries.search_fuzzy(s)
            c = matches[0] if matches else None
        return c.alpha_2 if c else None
    except Exception:
        return None


def _is_country_name(place_name: str) -> bool:
    """True if place_name is likely a country name (so geocode result without city = country-only)."""
    if not (place_name and place_name.strip()):
        return False
    key = place_name.strip().lower().replace(",", "").strip()
    if len(key) == 2 and key.isalpha():
        return True
    return _country_name_to_iso2(place_name) is not None


# Source -> country hint for geocoding (no import from ingest to avoid circular deps).
SOURCE_COUNTRY_HINT: dict[str, str | None] = {
    "espn_nfl": "United States", "espn_nba": "United States", "espn_mlb": "United States",
    "espn_nhl": "United States", "espn_ncf": "United States", "espn_ncb": "United States",
    "espn_ncaa": "United States", "espn_soccer": "United States", "espn_news": "United States",
    "bbc": "United Kingdom", "bbc_sport": "United Kingdom", "guardian_world": "United Kingdom",
    "guardian_football": "United Kingdom", "sky_sports_football": "United Kingdom",
    "nyt": "United States", "washingtonpost": "United States", "wsj": "United States",
    "reuters": None, "ap_news": None, "aljazeera": None,
}

# Minimal team mention -> team_key for stadium lookup when story has no team_home/team_away.
TEAM_MENTION_TO_KEY: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bnew orleans saints\b|\bsaints\b", re.I), "new-orleans-saints"),
    (re.compile(r"\blsu\b", re.I), "lsu-tigers-football"),
    (re.compile(r"\bflorida gators\b|\bgators\b", re.I), "florida-gators-football"),
    (re.compile(r"\btennessee volunteers\b|\bvolunteers\b", re.I), "tennessee-volunteers-football"),
    (re.compile(r"\bpenn state\b|\bnittany lions\b", re.I), "penn-state-nittany-lions-football"),
    (re.compile(r"\boklahoma sooners\b|\bsooners\b", re.I), "oklahoma-sooners-football"),
    (re.compile(r"\bflorida state\b|\bseminoles\b", re.I), "florida-state-seminoles-football"),
    (re.compile(r"\boregon ducks\b|\bducks\b.*(?:oregon|college)", re.I), "oregon-ducks-football"),
    (re.compile(r"\busc trojans\b|\btrojans\b.*(?:usc|southern cal)", re.I), "usc-trojans-football"),
    (re.compile(r"\btexas a&m\b|\baggies\b", re.I), "texas-am-aggies-football"),
    (re.compile(r"\bnebraska cornhuskers\b|\bcornhuskers\b", re.I), "nebraska-cornhuskers-football"),
    (re.compile(r"\bwisconsin badgers\b|\bbadgers\b", re.I), "wisconsin-badgers-football"),
    (re.compile(r"\bmiami hurricanes\b|\bhurricanes\b.*(?:miami|acc)", re.I), "miami-hurricanes-football"),
    (re.compile(r"\bnorth carolina tar heels\b|\btar heels\b", re.I), "north-carolina-tar-heels-football"),
    (re.compile(r"\bvirginia tech\b|\bhokies\b", re.I), "virginia-tech-hokies-football"),
    (re.compile(r"\bwashington huskies\b|\bhuskies\b.*(?:washington|pac)", re.I), "washington-huskies-football"),
    (re.compile(r"\boklahoma state\b", re.I), "oklahoma-state-cowboys-football"),
    (re.compile(r"\blakers\b", re.I), "los-angeles-lakers"),
    (re.compile(r"\bceltics\b", re.I), "boston-celtics"),
    (re.compile(r"\bcowboys\b", re.I), "dallas-cowboys"),
    (re.compile(r"\bpackers\b", re.I), "green-bay-packers"),
    (re.compile(r"\bmanchester united\b|\bman united\b", re.I), "manchester-united"),
    (re.compile(r"\bbarcelona\b|\bbarca\b", re.I), "barcelona"),
    (re.compile(r"\breal madrid\b", re.I), "real-madrid"),
]

ENTITY_EXTRACT_SYSTEM = """You extract structured entities from news text for a map application.

Output valid JSON only, with exactly these keys:
- "places": list of objects with "name" (string) and "type" (string: "city", "state", "region", "country", "province", "stadium"). Include ONLY geographic locations (cities, states, regions, countries, provinces, stadiums). Do NOT include person names.
- "people": list of objects with "name" (string). Include ONLY person names (players, coaches, politicians, etc.).
- "teams": list of objects with "name" (string), optional "sport" and "league". Include only sports teams/organizations.

Critical rules:
- If a word is BOTH a person's surname AND a country name (e.g. Jordan, Georgia, Congo), put it in "people" when the context clearly refers to a person (e.g. "Cameron Jordan", "Marcus Freeman") and in "places" ONLY when the context clearly refers to the country/region (e.g. "Jordan's economy", "travel to Jordan").
- When in doubt about a person vs place (e.g. "Jordan" could be the player or the country), prefer "people" if there is any mention of a person (player, coach, agent).
- Return "places" only for geographic locations. Do not put team names in "places"; put them in "teams".
- Output nothing else except the JSON object."""


def extract_entities(story: dict[str, Any]) -> dict[str, Any]:
    """
    Use LLM to extract places, people, and teams from story title + summary.
    Returns {"places": [...], "people": [...], "teams": [...]}. Only places are geocoded.
    """
    text = f"Title: {story.get('title', '')}\n\nSummary: {story.get('summary', '')}"
    if not text.strip():
        return {"places": [], "people": [], "teams": []}
    client = _client()
    if not client:
        return {"places": [], "people": [], "teams": []}
    try:
        resp = client.chat.completions.create(
            model=SUMMARY_MODEL,
            messages=[
                {"role": "system", "content": ENTITY_EXTRACT_SYSTEM},
                {"role": "user", "content": text[:6000]},
            ],
            max_tokens=500,
            temperature=0,
        )
        content = (resp.choices[0].message.content or "").strip()
        if not content:
            return {"places": [], "people": [], "teams": []}
        content = content.replace("```json", "").replace("```", "").strip()
        data = json.loads(content)
        places = data.get("places") or []
        people = data.get("people") or []
        teams = data.get("teams") or []
        return {"places": places if isinstance(places, list) else [], "people": people if isinstance(people, list) else [], "teams": teams if isinstance(teams, list) else []}
    except Exception as e:
        log.warning("Entity extraction failed: %s", e)
        return {"places": [], "people": [], "teams": []}


def geocode_place(name: str, country_hint: str | None = None) -> dict[str, Any] | None:
    """
    Geocode a place name. Uses cache when available. Returns
    {"lat", "lon", "display_name", "country", "region", "city"} or None.
    """
    if not (name and name.strip()):
        return None
    name = name.strip()
    query = f"{name}, {country_hint}" if country_hint else name
    cached = get_cached_geocode(query)
    if cached is not None:
        lat, lon, country = cached
        return {
            "lat": lat,
            "lon": lon,
            "display_name": name,
            "country": country,
            "region": None,
            "city": None,
        }
    try:
        geocoder = Nominatim(user_agent="pvdmaproom-news-map")
        result = geocoder.geocode(query, timeout=4, addressdetails=True)
    except (GeocoderServiceError, GeopyError):
        result = None
    if result is None:
        return None
    lat = float(result.latitude)
    lon = float(result.longitude)
    raw = result.raw if isinstance(result.raw, dict) else {}
    addr = raw.get("address") or {}
    country = addr.get("country") or (raw.get("address", {}).get("country") if isinstance(raw.get("address"), dict) else None)
    region = addr.get("state") or addr.get("region")
    city = addr.get("city") or addr.get("town") or addr.get("village")
    display_name = raw.get("display_name") or name
    set_cached_geocode(query, lat, lon, country)
    time.sleep(1)
    return {
        "lat": lat,
        "lon": lon,
        "display_name": display_name,
        "country": country,
        "region": region,
        "city": city,
    }


def derive_country_hint(story: dict[str, Any], entities: dict[str, Any]) -> str | None:
    """Derive a country hint from source and story context for geocoding bias."""
    source = (story.get("source") or "").strip().lower()
    if source and source in SOURCE_COUNTRY_HINT:
        hint = SOURCE_COUNTRY_HINT[source]
        if hint:
            return hint
    return None


def _infer_team_key_from_story(story: dict[str, Any]) -> str | None:
    """Infer a single team_key from story when team_home/team_away not set."""
    for pattern, team_key in TEAM_MENTION_TO_KEY:
        text = f"{story.get('title', '')} {story.get('summary', '')}"
        if pattern.search(text):
            return team_key
    return None


def stadium_location_from_story(story: dict[str, Any]) -> dict[str, Any] | None:
    """
    For sports stories: resolve team to stadium and return location dict.
    Uses story.team_home, story.team_away, or infers team from text.
    """
    for key in ("team_home", "team_away"):
        team_key = story.get(key)
        if team_key and isinstance(team_key, str):
            stadium = get_stadium_for_team(team_key.strip())
            if stadium:
                return stadium
    team_key = _infer_team_key_from_story(story)
    if team_key:
        stadium = get_stadium_for_team(team_key)
        if stadium:
            return stadium
    return None


def _is_sports_story(story: dict[str, Any]) -> bool:
    """True if story should use sports/stadium location logic."""
    if story.get("topic") == "sports":
        return True
    source = (story.get("source") or "").strip().lower()
    return source in {
        "espn_news", "espn_nfl", "espn_nba", "espn_mlb", "espn_nhl", "espn_soccer",
        "espn_ncf", "espn_ncb", "espn_ncaa", "espn_tennis", "on3", "nbcsports",
        "the_athletic", "bbc_sport", "sky_sports_football", "guardian_football",
    }


def attach_location(story: dict[str, Any]) -> dict[str, Any]:
    """
    Unified location pipeline: adds story['lat'], story['lon'], and optionally
    story['country'], story['region'], story['city'], story['place_name']
    using topic-aware geocoding. Does not geocode person names.
    """
    # 1. Sports fast-path: use team/stadium (city-level)
    if _is_sports_story(story):
        loc = stadium_location_from_story(story)
        if loc:
            story["lat"] = float(loc.get("lat", 0))
            story["lon"] = float(loc.get("lon", 0))
            story["place_name"] = loc.get("stadium_name") or loc.get("city") or ""
            story["city"] = loc.get("city")
            story["country"] = loc.get("country") or "United States"
            story["country_code"] = _country_name_to_iso2(story["country"]) or "US"
            story["location_type"] = "city"
            story["region"] = None
            if not story.get("place"):
                story["place"] = story.get("place_name") or story.get("city") or story.get("country")
            return story

    # 2. Entity extraction (people vs places vs teams)
    entities = extract_entities(story)
    people_last_names = set()
    for p in entities.get("people", []):
        name = (p.get("name") or "").strip()
        if name:
            parts = name.split()
            if parts:
                people_last_names.add(parts[-1].strip())

    # 3. Filter places: drop any that match a person's last name (e.g. Jordan from Cameron Jordan)
    def _place_priority(p: dict[str, Any]) -> int:
        t = (p.get("type") or "").lower()
        if t in ("city", "stadium"):
            return 0
        if t in ("state", "region", "province"):
            return 1
        return 2

    filtered_places = []
    for place in entities.get("places", []):
        name = (place.get("name") or "").strip()
        if not name or name in people_last_names:
            continue
        filtered_places.append({"name": name, "type": place.get("type")})
    filtered_places.sort(key=_place_priority)
    seen: set[str] = set()
    dedup = []
    for p in filtered_places:
        n = p["name"]
        if n not in seen:
            seen.add(n)
            dedup.append(n)

    # 4. Country hint
    country_hint = derive_country_hint(story, entities)

    # 5. Geocode first successful candidate; classify city vs country-only
    for name in dedup[:8]:
        result = geocode_place(name, country_hint=country_hint)
        if not result:
            continue
        country_name = result.get("country")
        country_code = _country_name_to_iso2(country_name) if country_name else None
        city = result.get("city")
        region = result.get("region")
        has_city_or_region = bool(city and str(city).strip()) or bool(region and str(region).strip())
        is_country_place = _is_country_name(name)
        if has_city_or_region or not is_country_place:
            story["lat"] = result["lat"]
            story["lon"] = result["lon"]
            story["country"] = country_name
            story["country_code"] = country_code
            story["location_type"] = "city"
            story["region"] = region
            story["city"] = city
            story["place_name"] = result.get("display_name", name)
            if not story.get("place"):
                story["place"] = story.get("place_name") or name
            return story
        else:
            story["lat"] = None
            story["lon"] = None
            story["country"] = country_name
            story["country_code"] = country_code
            story["location_type"] = "country"
            story["city"] = None
            story["region"] = region
            story["place_name"] = None
            if not story.get("place"):
                story["place"] = country_name or name
            return story

    return story
