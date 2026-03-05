"""Ingestion entrypoint: fetch stories, geocode, and store in SQLite."""

from __future__ import annotations

import logging
import os
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any
from urllib.parse import urlparse

from geopy.exc import GeocoderServiceError, GeopyError
from geopy.geocoders import Nominatim

from app.db import (
    get_cached_geocode,
    get_db_path,
    get_story_count_by_country,
    get_total_mapped_story_count,
    init_db,
    set_cached_geocode,
    upsert_article_related_video,
    upsert_country_fact,
    upsert_country_name,
    upsert_rankings,
    upsert_story,
)
from app.country_names import fetch_country_name_index
from app.economist_rankings import build_rankings_for_db
from app.factbook import (
    build_country_facts_index,
    load_factbook,
    lookup_country_fact,
    normalize_country_name,
)
from app.ai_summary import generate_ai_title
from app.location_inference import infer_relevant_countries
from app.sources.world_feeds import fetch_all_world_sources
from app.sources.x_reports import fetch_verified_x_reports
from app.sources.nyt import fetch_nyt_top_stories
from app.sources.economist_podcast import fetch_economist_podcast

MAX_INGEST_STORIES = 5000
# Regex patterns for simple place extraction.
PAREN_PLACE_RE = re.compile(r"\(([A-Z][A-Za-z .'-]{1,60})\)")
IN_PLACE_RE = re.compile(r"\b(?:in|at|near|from)\s+([A-Z][A-Za-z .'-]{1,60})")
LEADING_COLON_RE = re.compile(r"^\s*([A-Z][A-Za-z .'-]{1,60})\s*:")
EVENT_PREFIX_RE = re.compile(
    r"\b([A-Z][A-Za-z .'-]{1,40})\s+"
    r"(?:war|conflict|floods?|earthquake|election|protests?|crisis|offensive)\b"
)
DATELINE_RE = re.compile(r"^\s*([A-Z][A-Za-z .'-]{1,60})\s*(?:,|-|\()")

# Domains we treat as "news article" links when found inside an X post (verified relation).
NEWS_ARTICLE_DOMAINS = frozenset({
    "bbc.com", "www.bbc.com", "bbc.co.uk", "reuters.com", "www.reuters.com",
    "nytimes.com", "www.nytimes.com", "washingtonpost.com", "www.washingtonpost.com",
    "theguardian.com", "www.theguardian.com", "economist.com", "www.economist.com",
    "wsj.com", "www.wsj.com", "axios.com", "www.axios.com", "aljazeera.com", "www.aljazeera.com",
    "dw.com", "cnn.com", "www.cnn.com", "nbcnews.com", "www.nbcnews.com", "sky.com", "news.sky.com",
    "politico.com", "www.politico.com", "middleeasteye.net", "www.middleeasteye.net",
    "rudaw.net", "www.rudaw.net", "apnews.com", "www.apnews.com", "thetimes.co.uk",
    "amnesty.org", "hrw.org", "carnegieendowment.org", "aei.org", "hudson.org",
})
LINK_IN_TEXT_RE = re.compile(r"https?://[^\s\"'<>)\]]+")

INVALID_PLACE_TERMS = {
    "reuters",
    "bbc",
    "cnn",
    "nbc",
    "sky news",
    "espn",
    "substack",
    "jamestown",
    "rudaw",
    "middle east eye",
    "abc",
    "on3",
    "the athletic",
    "axios",
    "wsj",
    "washington post",
    "new york times",
    "the economist",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
}
COUNTRY_ALIAS_TO_NAME = {
    "britain": "United Kingdom",
    "russian": "Russia",
    "russian federation": "Russia",
    "myanmar": "Myanmar",
    "burma": "Myanmar",
    "czech republic": "Czechia",
    "dr congo": "Democratic Republic of the Congo",
    "congo drc": "Democratic Republic of the Congo",
    "ivory coast": "Cote d'Ivoire",
    "east timor": "Timor-Leste",
    "iran": "Iran",
    "north western iran": "Iran",
    "northwestern iran": "Iran",
    "western iran": "Iran",
    "northern iran": "Iran",
    "kurdistan": "Iraq",
    "iraqi kurdistan": "Iraq",
}
SOURCE_DEFAULT_COUNTRY = {
    "irrawaddy_myanmar": "Myanmar",
    "gov_us_dod_releases": "United States",
    "gov_us_dod_contracts": "United States",
    "gov_uk_announcements": "United Kingdom",
    "gov_eu_commission": None,  # EU: multi-country, no single default
    "gov_canada_news": "Canada",
    "gov_canada_pm": "Canada",
    "gov_canada_global_affairs": "Canada",
    "gov_brazil_planalto": "Brazil",
    "gov_argentina_presidencia": "Argentina",
    "gov_chile_presidencia": "Chile",
    "gov_colombia_presidencia": "Colombia",
    "gov_mexico_presidencia": "Mexico",
    "gov_peru_pcm": "Peru",
    "gov_japan_kantei": "Japan",
    "gov_japan_mof": "Japan",
    "gov_india_mea": "India",
    "gov_singapore_mfa": "Singapore",
    "gov_south_korea_yonhap": "South Korea",
    "gov_indonesia_kemlu": "Indonesia",
    "gov_malaysia_pmo": "Malaysia",
    "gov_philippines_dfa": "Philippines",
    "gov_thailand_mfa": "Thailand",
    "gov_vietnam_mofa": "Vietnam",
    "gov_russia_kremlin": "Russia",
    "gov_kazakhstan_pm": "Kazakhstan",
    "gov_uzbekistan_mfa": "Uzbekistan",
    "gov_south_africa": "South Africa",
    "gov_nigeria_fmino": "Nigeria",
    "gov_kenya_president": "Kenya",
    "gov_egypt_sis": "Egypt",
    "gov_ethiopia_pmo": "Ethiopia",
    "gov_ghana_presidency": "Ghana",
    "gov_tanzania_presidency": "Tanzania",
    "gov_morocco_map": "Morocco",
    "gov_senegal_presidency": "Senegal",
    "gov_au_commission": None,  # African Union: multi-country
    "gov_australia_pm": "Australia",
    "gov_australia_rba": "Australia",
    "gov_new_zealand_beehive": "New Zealand",
    "abc_news": "United States",
    "cnn": "United States",
        "reuters": None,  # Global - no single default country
    "ap_news": None,  # Global - Associated Press
    "bbc": "United Kingdom",
    "bbc_world": "United Kingdom",
    "nyt": "United States",
    "washingtonpost": "United States",
    "wsj": "United States",
    "economist": "United Kingdom",
    "ft": "United Kingdom",  # Financial Times
    "guardian": "United Kingdom",
    "aljazeera": None,  # Pan-Middle East
        "dw": "Germany",

    "france24": "France",
    "tass": "Russia",
    "rt": "Russia",
    "xinhua": "China",
    "cgtn": "China",
    "nbc": "United States",
    "on3": "United States",
    "nbcsports": "United States",
        "the_athletic": "United States",
        "axios": "United States",
    "usa_today": "United States",
    "politico": "United States",
    "the_hill": "United States",
    "npr": "United States",
    "pbs": "United States",
    "cbsnews": "United States",
    "independent": "United Kingdom",
    "telegraph": "United Kingdom",
        "times_of_india": "India",
    "sky_news": "United Kingdom",
    "espn_news": "United States",
    "espn_nfl": "United States",
    "espn_nba": "United States",
    "espn_mlb": "United States",
    "espn_nhl": "United States",
    "espn_soccer": "United States",
    "espn_ncf": "United States",
    "espn_ncb": "United States",
    "espn_ncaa": "United States",
    "espn_tennis": "United States",
    "substack_rochan": "Ukraine",
    "substack_counteroffensive": "Ukraine",
    "substack_warwickpowell": "Ukraine",
    "substack_professorbonk": "Ukraine",
    "rudaw_english": "Iraq",  # Kurdistan / Iraq focus
    "middle_east_eye": None,  # Pan–Middle East
}
UNDER_REPORTED_PRIORITY_TERMS = {
    # Great Lakes + Central/East Africa
    "drc",
    "democratic republic of the congo",
    "congo",
    "rwanda",
    "burundi",
    "uganda",
    "south sudan",
    "sudan",
    "darfur",
    # Sahel + West/Central Africa
    "sahel",
    "mali",
    "niger",
    "burkina faso",
    "chad",
    "cameroon",
    "central african republic",
    "car",
    "cabo delgado",
    "mozambique",
    # Horn + Red Sea + North Africa
    "somalia",
    "ethiopia",
    "eritrea",
    "djibouti",
    "yemen",
    "gaza",
    "west bank",
    "palestinian",
    "syria",
    "lebanon",
    "libya",
    # Southeast Asia / Indo-Pacific
    "myanmar",
    "burma",
    "asean",
    "south china sea",
    "philippines",
    "vietnam",
    "thailand",
    "laos",
    "cambodia",
    "indonesia",
    "malaysia",
    "papua",
    "timor leste",
    "taiwan strait",
}
HUMANITARIAN_CONFLICT_TERMS = {
    "displaced",
    "refugee",
    "humanitarian",
    "famine",
    "aid",
    "cholera",
    "outbreak",
    "militia",
    "massacre",
    "ceasefire",
    "peacekeeping",
    "insurgency",
    "junta",
    "separatist",
    "guerrilla",
    "ethnic armed group",
    "paramilitary",
}
MAJOR_ISSUE_TERMS = {
    "war",
    "conflict",
    "earthquake",
    "flood",
    "famine",
    "pandemic",
    "outbreak",
    "election",
    "coup",
    "sanctions",
    "nuclear",
    "cyberattack",
    "inflation",
    "recession",
    "food prices",
    "migration",
    "climate",
    "heatwave",
    "wildfire",
    "civil war",
    "rebels",
    "insurgency",
    "separatist",
    "border clash",
    "naval standoff",
    "maritime dispute",
    "junta",
    "coup",
}


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

    # Pattern: "Paris, ...", "Cairo - ...", "(Reuters) ..."
    dateline = DATELINE_RE.search(text)
    if dateline:
        candidates.append(dateline.group(1).strip())

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
        cleaned = candidate.strip(" .,:;()[]{}")
        key = cleaned.lower()
        if not _is_valid_place_candidate(cleaned):
            continue
        if key in seen:
            continue
        deduped.append(cleaned)
        seen.add(key)

    return deduped


def _is_valid_place_candidate(candidate: str) -> bool:
    """Reject obvious non-place terms from headline regex extraction."""
    key = candidate.strip().lower()
    if not key:
        return False
    if key in INVALID_PLACE_TERMS:
        return False
    if any(ch.isdigit() for ch in key):
        return False
    if key.startswith("the "):
        return False
    words = [w for w in key.split(" ") if w]
    if len(words) > 4:
        return False
    return True


def _extract_explicit_country(
    story: dict[str, Any], country_patterns: list[tuple[re.Pattern[str], str]]
) -> str | None:
    """Find direct country mentions in title/summary with normalized country output."""
    text = f"{story.get('title', '')} {story.get('summary', '')}"
    if re.search(r"(?:\bUS\b|\bUSA\b|\bU\.S\.)", text):
        return "United States"
    if re.search(r"(?:\bUK\b|\bU\.K\.)", text):
        return "United Kingdom"

    lower_text = text.lower()

    for alias, canonical in COUNTRY_ALIAS_TO_NAME.items():
        if re.search(rf"\b{re.escape(alias)}\b", lower_text):
            return canonical

    for pattern, country_name in country_patterns:
        if pattern.search(text):
            return country_name
    return None


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


def _geocode_place(geocoder: Nominatim, place: str) -> tuple[float, float, str | None] | None:
    """Geocode with persistent cache to avoid duplicate requests."""
    cached = get_cached_geocode(place)
    if cached is not None:
        return cached

    try:
        result = geocoder.geocode(place, timeout=4)
    except (GeocoderServiceError, GeopyError):
        result = None

    if result is None:
        return None

    coords = (float(result.latitude), float(result.longitude))
    country = (
        result.raw.get("address", {}).get("country")
        if isinstance(result.raw, dict)
        else None
    )

    set_cached_geocode(place, coords[0], coords[1], country)
    return coords[0], coords[1], country


def _resolve_story_location(
    geocoder: Nominatim,
    story: dict[str, Any],
    country_patterns: list[tuple[re.Pattern[str], str]],
) -> tuple[str, float, float, str | None] | None:
    """
    Resolve best-effort event location.
    """
    explicit_country = _extract_explicit_country(story, country_patterns)
    if not explicit_country:
        explicit_country = SOURCE_DEFAULT_COUNTRY.get(
            str(story.get("source", "")).lower()
        )
    if explicit_country:
        coords = _geocode_place(geocoder, explicit_country)
        if coords is not None:
            return explicit_country, coords[0], coords[1], coords[2] or explicit_country

    # Keep geocoding bounded to avoid very slow ingest runs.
    
        coords = _geocode_place(geocoder, candidate)
        if coords is not None:
            return candidate, coords[0], coords[1], coords[2]

    return None


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


# Primary news sources: process first to maximize map coverage from trusted outlets.
_PRIMARY_NEWS_SOURCES = frozenset({
    "bbc", "bbc_asia", "bbc_africa", "bbc_middle_east",
    "reuters", "economist", "economist_asia", "economist_mea",
    "nyt", "washingtonpost", "wsj", "guardian_world", "guardian_international",
    "aljazeera", "axios", "politico", "dispatch", "dw_world", "abc_news",
    "cnn", "nbc", "sky_news",
    "espn_news", "espn_nfl", "espn_nba", "espn_mlb", "espn_nhl", "espn_soccer",
    "espn_ncf", "espn_ncb", "espn_ncaa", "espn_tennis",
    "on3", "nbcsports", "the_athletic",
})


def _priority_score(story: dict[str, Any]) -> int:
    """Score stories so news sources and underreported regions are prioritized."""
    text = f"{story.get('title', '')} {story.get('summary', '')}".lower()
    score = 0

    source = str(story.get("source", "")).lower()
    if source in _PRIMARY_NEWS_SOURCES:
        score += 8

    for term in UNDER_REPORTED_PRIORITY_TERMS:
        if term in text:
            score += 4
    for term in HUMANITARIAN_CONFLICT_TERMS:
        if term in text:
            score += 2
    for term in MAJOR_ISSUE_TERMS:
        if term in text:
            score += 2

    if source in {
        "bbc_africa",
        "bbc_middle_east",
        "bbc_asia",
        "economist_mea",
        "economist_asia",
        "economist_graphic_detail",
        "guardian_world",
        "guardian_international",
        "dispatch",
        "politico",
        "amnesty",
        "hrw",
        "aljazeera",
        "dw_world",
        "abc_news",
        "cnn",
        "nbc",
        "sky_news",
        "on3",
        "nbcsports",
        "the_athletic",
        "espn_news",
        "espn_nfl",
        "espn_nba",
        "espn_mlb",
        "espn_nhl",
        "espn_soccer",
        "espn_ncf",
        "espn_ncb",
        "espn_ncaa",
        "espn_tennis",
        "substack_jamestown",
        "substack_rochan",
        "substack_counteroffensive",
        "substack_warwickpowell",
        "substack_professorbonk",
        "irrawaddy_myanmar",
        "carnegie",
        "aei",
        "hudson",
        "rudaw_english",
        "middle_east_eye",
    } or source.startswith("gov_") or source in {
        "x_isw", "x_liveuamap", "x_carnegie", "x_hudson",
        "x_barakravid", "x_clarissaward", "x_richardengel", "x_lynsaddler",
        "x_nickpatonwalsh", "x_borzsandor", "x_ianbremmer",
        "x_rudaw", "x_middleeasteye", "x_kurdistan24",
    }:
        score += 4
    if source.startswith("x_"):
        score += 3
    return score


def _rank_and_limit_stories(stories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Prioritize underreported regions while keeping source diversity.
    """
    ranked = sorted(
        stories,
        key=lambda s: (_priority_score(s), str(s.get("published_at", ""))),
        reverse=True,
    )
    # Keep all fetched stories, only sorted by priority/time.
    return ranked[:MAX_INGEST_STORIES]


def _is_highly_relevant(
    story: dict[str, Any], country: str, place: str, min_score: int = 2
) -> bool:
    """
    Require country/place relevance before pinning. min_score=1 for broader coverage (e.g. empty countries).
    """
    text = f"{story.get('title', '')} {story.get('summary', '')}".lower()
    country_norm = normalize_country_name(country)
    place_norm = normalize_country_name(place)

    score = 0
    country_terms: list[str] = [country.lower()]
    # Include known aliases that map to this resolved country.
    for alias, canonical in COUNTRY_ALIAS_TO_NAME.items():
        if normalize_country_name(canonical) == country_norm:
            country_terms.append(alias.lower())
    # Add a few important edge terms.
    if country_norm == normalize_country_name("Democratic Republic of the Congo"):
        country_terms.extend(["drc", "dr congo", "congo"])
    if country_norm == normalize_country_name("United States"):
        country_terms.extend(["u.s.", "usa", "us"])
    if country_norm == normalize_country_name("United Kingdom"):
        country_terms.extend(["u.k.", "uk", "britain"])

    if any(term and term in text for term in country_terms):
        score += 3
    if place and place.lower() in text:
        score += 2
        # Place mention with successful geocoded country is strong relevance.
        if country:
            score += 1
    if place_norm and place_norm == country_norm:
        score += 1
    # If story includes major conflict/geopolitics signal and has resolved country,
    # allow slightly lower lexical threshold to avoid missing key Russia/war updates.
    if country and any(term in text for term in MAJOR_ISSUE_TERMS):
        score += 1
    default_country = SOURCE_DEFAULT_COUNTRY.get(str(story.get("source", "")).lower(), "")
    if default_country and normalize_country_name(default_country) == country_norm:
        score += 2
    elif default_country and default_country == country:
        score += 2

    return score >= min_score


def _canonical_x_url(url: str) -> str:
    """Convert nitter/mirror URL to x.com for embedding."""
    if not url:
        return url
    u = url.strip()
    if "nitter." in u.lower() or "nitter.net" in u.lower():
        u = re.sub(r"^https?://nitter[^/]*", "https://x.com", u, flags=re.IGNORECASE)
    u = re.sub(r"^https?://(twitter\.com)", r"https://x.com", u, flags=re.IGNORECASE)
    return u


def _title_is_url_or_empty(title: str | None) -> bool:
    """True if the title is empty or is effectively a URL (should be replaced by AI title)."""
    if not title or not title.strip():
        return True
    t = title.strip()
    if t.startswith("http://") or t.startswith("https://"):
        return True
    if re.match(r"^[\w.-]+\.(com|org|net|io|co|uk|de|fr)/", t, re.IGNORECASE):
        return True
    return False


def _ensure_display_title(story: dict[str, Any]) -> None:
    """If the story title is a URL or empty, generate an AI headline and set display_title."""
    if story.get("display_title"):
        return
    if not _title_is_url_or_empty(story.get("title")):
        return
    summary = (story.get("summary") or "").strip()
    fallback = (story.get("title") or story.get("url") or "").strip()
    try:
        ai_title = generate_ai_title(summary, fallback)
        if ai_title:
            story["display_title"] = ai_title
    except Exception:
        pass


def _record_article_video_links_if_x(story: dict[str, Any]) -> None:
    """When an X post links to a news article, record that so we can embed the video only for that article (verified)."""
    source = str(story.get("source", "")).strip().lower()
    if not source.startswith("x_"):
        return
    summary = story.get("summary") or ""
    video_url = _canonical_x_url(story.get("url") or "")
    if not video_url:
        return
    for match in LINK_IN_TEXT_RE.finditer(summary):
        link = match.group(0).rstrip(".,;:)")
        try:
            netloc = (urlparse(link).netloc or "").lower()
            if not netloc:
                continue
            domain = netloc[4:] if netloc.startswith("www.") else netloc
            if domain in NEWS_ARTICLE_DOMAINS or f"www.{domain}" in NEWS_ARTICLE_DOMAINS:
                upsert_article_related_video(link, video_url)
        except Exception:
            continue


def run_ingest() -> None:
    """Fetch all enabled sources and insert stories into SQLite."""
    init_db()
    geocoder = _get_geocoder()
    try:
        factbook_payload = load_factbook()
        factbook_index = build_country_facts_index(factbook_payload)
    except Exception:
        # Keep ingestion alive if the external Factbook source is unavailable.
        factbook_index = {}
    for fact in factbook_index.values():
        upsert_country_fact(fact)
    try:
        country_name_index = fetch_country_name_index()
    except Exception:
        country_name_index = {}
    for names in country_name_index.values():
        upsert_country_name(names["english_name"], names["original_name"])
    try:
        ranking_rows = build_rankings_for_db()
        if ranking_rows:
            upsert_rankings(ranking_rows)
    except Exception:
        pass
    country_patterns = [
        (re.compile(rf"\b{re.escape(item.get('country_name', ''))}\b", re.IGNORECASE), item.get("country_name", ""))
        for item in factbook_index.values()
        if item.get("country_name")
    ]
    country_patterns.sort(key=lambda x: len(x[1]), reverse=True)

    raw_incoming = fetch_all_world_sources()
    nyt_key = os.getenv("NYT_API_KEY", "").strip()
    if nyt_key:
        try:
            raw_incoming.extend(fetch_nyt_top_stories(nyt_key))
        except Exception:
            pass  # NYT API optional; RSS feed still provides some NYT content
    try:
        raw_incoming.extend(fetch_verified_x_reports())
    except Exception:
        # Continue without X reports when mirrors are unavailable.
        pass
    try:
        raw_incoming.extend(fetch_economist_podcast())
    except Exception:
        pass
    incoming = [s for s in (_sanitize_story(x) for x in raw_incoming) if s is not None]
    incoming = _rank_and_limit_stories(incoming)

    # Prioritize coverage: prefer countries with no pins; ensure minimum 100 pins.
    initial_counts = get_story_count_by_country()
    initial_total = get_total_mapped_story_count()
    added_this_run: dict[str, int] = {}
    total_added = 0

    def _min_score_for(country: str) -> int:
        norm = normalize_country_name(country)
        if not norm:
            return 2
        pins_in_country = initial_counts.get(norm, 0) + added_this_run.get(norm, 0)
        total_pins = initial_total + total_added
        if pins_in_country == 0 or total_pins < 100:
            return 1
        return 2

    def _record_added(country: str) -> None:
        nonlocal total_added
        norm = normalize_country_name(country)
        if norm:
            added_this_run[norm] = added_this_run.get(norm, 0) + 1
        total_added += 1

    for story in incoming:
        if story.get("source") == "economist_podcast":
            story["place"] = "World"
            story["country"] = "World"
            story["lat"] = 20.0
            story["lon"] = 0.0
            _ensure_display_title(story)
            upsert_story(story)
            continue
        resolved = _resolve_story_location(geocoder, story, country_patterns)
        if resolved is not None:
            place, lat, lon, country = resolved
            min_score = _min_score_for(country)
            if country and _is_highly_relevant(story, country, place, min_score=min_score):
                story["place"] = place
                story["country"] = country
                story["lat"] = lat
                story["lon"] = lon
                _ensure_display_title(story)
                upsert_story(story)
                _record_added(country)
                _record_article_video_links_if_x(story)
                fact = lookup_country_fact(factbook_index, country)
                if fact is not None:
                    upsert_country_fact(fact)
            continue

        # Location could not be resolved: use model to infer relevant countries and add only there.
        try:
            countries = infer_relevant_countries(story)
        except Exception:
            countries = []
        for country_name in countries[:5]:
            if not (country_name and country_name.strip()):
                continue
            country_name = country_name.strip()
            coords = _geocode_place(geocoder, country_name)
            if coords is None:
                continue
            lat, lon, country_from_geocode = coords
            country = country_from_geocode or country_name
            story["place"] = country_name
            story["country"] = country
            story["lat"] = lat
            story["lon"] = lon
            min_score = _min_score_for(country)
            if not _is_highly_relevant(story, country, country_name, min_score=min_score):
                continue
            _ensure_display_title(story)
            upsert_story(story)
            _record_added(country)
            _record_article_video_links_if_x(story)
            fact = lookup_country_fact(factbook_index, country)
            if fact is not None:
                upsert_country_fact(fact)

    count = get_total_mapped_story_count()
    logging.getLogger(__name__).info(
        "Ingest finished: %s mapped stories (db_path=%s)",
        count,
        get_db_path(),
    )


if __name__ == "__main__":
    run_ingest()

