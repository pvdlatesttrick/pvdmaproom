"""
Generate AI summaries with broader context for a country or a news story.
Supports OpenAI (OPENAI_API_KEY) or Groq free tier (GROQ_API_KEY) automatically.

Policy: Summaries are based on the model's knowledge and on provided context (e.g. CIA facts);
they must not be driven by or reproduce Wikipedia content. Wikipedia is used elsewhere only
for map data (e.g. historical pins, under-reported country facts), not for full summaries.
"""
from __future__ import annotations
import logging
import os
from typing import Any

from app.topics import TOPIC_DEFINITIONS, TOPIC_LABELS, TOPIC_PRIORITY

log = logging.getLogger(__name__)

# --- API key resolution ---
# Priority: OPENAI_API_KEY > GROQ_API_KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip()

if OPENAI_API_KEY:
    _ACTIVE_KEY = OPENAI_API_KEY
    _ACTIVE_BASE_URL = OPENAI_BASE_URL or None
    _DEFAULT_MODEL = "gpt-4o-mini"
elif GROQ_API_KEY:
    _ACTIVE_KEY = GROQ_API_KEY
    _ACTIVE_BASE_URL = "https://api.groq.com/openai/v1"
    _DEFAULT_MODEL = "llama-3.3-70b-versatile"
else:
    _ACTIVE_KEY = ""
    _ACTIVE_BASE_URL = None
    _DEFAULT_MODEL = "gpt-4o-mini"

SUMMARY_MODEL = os.getenv("SUMMARY_MODEL", os.getenv("LOCATION_MODEL", _DEFAULT_MODEL)).strip()

COUNTRY_SYSTEM = """You are a concise analyst. Given a country name and optional basic facts (capital, population, etc.), write a short summary (2-4 sentences) that gives broader context: current relevance in the news, key geopolitical or economic themes, and why the country matters right now. Use neutral, factual language. Base your summary on your own knowledge and the facts provided; do not reproduce or paraphrase Wikipedia. Output only the summary text, no headings or bullet points."""

# Map tab -> focus instruction for country summary (from app.topics TOPIC_DEFINITIONS).
COUNTRY_MAP_FOCUS = {
    k: f"Focus this summary strictly on: {v} Apply this to the country only; do not discuss other topics unless directly relevant."
    for k, v in TOPIC_DEFINITIONS.items()
}

STORY_SYSTEM = """You are a concise analyst. Given a news story's title and summary, write a short summary (2-4 sentences) that: (1) briefly states what the story is about, and (2) adds broader context - why it matters, background, or how it fits into larger developments. Use neutral, factual language. Base your summary on the story and your knowledge; do not reproduce Wikipedia. If the story is about a specific country or region, mention that. Output only the summary text, no headings or bullet points."""

TITLE_SYSTEM = """You write short headlines for news articles and social posts. Given the article or post content (and optional URL or raw title), output a single clear headline in sentence case. One line only, no quotes, no period at the end. Do not output a URL or repeat the URL. Maximum about 80 characters. Be specific and factual."""

CLASSIFIER_SYSTEM = """
You are a classifier that assigns ONE primary topic label to a news story.

Available labels and definitions:
- economics: {econ}
- geopolitics: {geo}
- conflicts: {conf}
- sports: {sports}

Rules:
- Output ONLY one word: economics, geopolitics, conflicts, or sports.
- If a story fits multiple labels, use this priority order:
  conflicts > geopolitics > economics > sports.
""".format(
    econ=TOPIC_DEFINITIONS["economics"],
    geo=TOPIC_DEFINITIONS["geopolitics"],
    conf=TOPIC_DEFINITIONS["conflicts"],
    sports=TOPIC_DEFINITIONS["sports"],
)


def _client():
    """Return OpenAI-compatible client or None if not configured."""
    if not _ACTIVE_KEY:
        return None
    try:
        import openai
    except ImportError:
        return None
    kwargs: dict[str, Any] = {"api_key": _ACTIVE_KEY}
    if _ACTIVE_BASE_URL:
        kwargs["base_url"] = _ACTIVE_BASE_URL
    return openai.OpenAI(**kwargs)


def _year_label(year: int | None) -> str:
    """Format year for prompts (e.g. 1979, 1000 BC)."""
    if year is None:
        return ""
    if year < 1:
        return f" {abs(year)} BC"
    return f" {year}"


def summarize_country(
    country_name: str,
    facts: dict[str, Any] | None = None,
    map_key: str | None = None,
    year: int | None = None,
) -> str | None:
    """Return an AI-generated summary for the country, optionally focused on map tab and/or a specific year (for historical view)."""
    if not country_name or not country_name.strip():
        return None
    client = _client()
    if not client:
        return None
    facts_text = ""
    if facts:
        parts = [f"{k}: {v}" for k, v in facts.items() if v]
        if parts:
            facts_text = "\nFacts: " + "; ".join(parts[:8])
    focus_instruction = ""
    if map_key and (map_key or "").strip().lower() in COUNTRY_MAP_FOCUS:
        focus_instruction = "\n\n" + COUNTRY_MAP_FOCUS[(map_key or "").strip().lower()]
    year_instruction = ""
    if year is not None:
        ylab = _year_label(year)
        year_instruction = (
            f"\n\nThe user is viewing the map for the year{ylab}. "
            "Focus your summary entirely on what was happening in this country in that year: "
            "major events, politics, conflicts, sports (e.g. Olympics, World Cup), economy, and culture. "
            "Be specific to that year; do not describe the present day."
        )
    user_content = f"Country: {country_name.strip()}{facts_text}{focus_instruction}{year_instruction}\n\nWrite the summary:"
    try:
        resp = client.chat.completions.create(
            model=SUMMARY_MODEL,
            messages=[
                {"role": "system", "content": COUNTRY_SYSTEM},
                {"role": "user", "content": user_content},
            ],
            max_tokens=400,
            temperature=0.3,
        )
        text = (resp.choices[0].message.content or "").strip()
        return text if text else None
    except Exception as e:
        log.warning("Country summary API call failed: %s", e)
        return None


def summarize_story(
    title: str,
    summary: str,
    country: str | None = None,
    source: str | None = None,
) -> str | None:
    """Return an AI-generated summary and broader context for the story, or None if unavailable."""
    if not title and not summary:
        return None
    client = _client()
    if not client:
        return None
    extra = []
    if country:
        extra.append(f"Place/country: {country}")
    if source:
        extra.append(f"Source: {source}")
    user_content = f"Title: {title or '(no title)'}\n\nSummary: {(summary or '')[:1200]}"
    if extra:
        user_content += "\n\n" + "; ".join(extra)
    user_content += "\n\nWrite the summary with broader context:"
    try:
        resp = client.chat.completions.create(
            model=SUMMARY_MODEL,
            messages=[
                {"role": "system", "content": STORY_SYSTEM},
                {"role": "user", "content": user_content},
            ],
            max_tokens=400,
            temperature=0.3,
        )
        text = (resp.choices[0].message.content or "").strip()
        return text if text else None
    except Exception as e:
        log.warning("Story summary API call failed: %s", e)
        return None


VALID_TOPIC_LABELS = frozenset(TOPIC_LABELS)


def classify_topic(client: Any, title: str, summary: str) -> str:
    """Assign ONE primary topic label via the classifier LLM. Defaults to 'geopolitics' if response is invalid."""
    text = f"Title: {title}\n\nSummary: {summary}"
    resp = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": CLASSIFIER_SYSTEM},
            {"role": "user", "content": text},
        ],
        max_tokens=2,
        temperature=0,
    )
    label = (resp.choices[0].message.content or "").strip().lower()
    return label if label in VALID_TOPIC_LABELS else "geopolitics"


def classify_story(story: dict[str, Any] | None) -> str | None:
    """
    Assign ONE primary topic label to a news story using the classifier LLM.
    Returns one of: economics, geopolitics, conflicts, sports; or None if API unavailable.
    """
    if not story:
        return None
    title = (story.get("title") or "").strip()
    summary = (story.get("summary") or "").strip()
    if not title and not summary:
        return None
    client = _client()
    if not client:
        return None
    try:
        return classify_topic(client, title or "(no title)", (summary or "")[:800])
    except Exception as e:
        log.warning("Story classifier API call failed: %s", e)
        return None


def generate_ai_title(summary: str, fallback: str = "") -> str | None:
    """Generate a short headline from article/post content. Use when the original title is a URL or empty."""
    content = (summary or "").strip()[:1500]
    if not content:
        return None
    client = _client()
    if not client:
        return None
    user = f"Content:\n{content}"
    if fallback:
        user += f"\n\n(Original title or link was: {fallback[:200]})"
    user += "\n\nHeadline:"
    try:
        resp = client.chat.completions.create(
            model=SUMMARY_MODEL,
            messages=[
                {"role": "system", "content": TITLE_SYSTEM},
                {"role": "user", "content": user},
            ],
            max_tokens=120,
            temperature=0.3,
        )
        text = (resp.choices[0].message.content or "").strip()
        if not text:
            return None
        return text.split("\n")[0].strip()[:200]
    except Exception as e:
        log.warning("AI title generation failed: %s", e)
        return None
