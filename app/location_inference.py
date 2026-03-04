"""
Infer relevant countries for a story using an LLM when geocoding fails.
Only adds the story to the map where it is relevant.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

log = logging.getLogger(__name__)

# Optional: OPENAI_API_KEY or OPENAI_BASE_URL for compatible APIs
LOCATION_MODEL = os.getenv("LOCATION_MODEL", "gpt-4o-mini").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip()  # e.g. for Azure or proxy


SYSTEM_PROMPT = """You are a geography classifier for news articles. Given the title and summary of a news story, output a JSON array of country names (English, as commonly used e.g. "United States", "Iran", "Ukraine") that the article is directly relevant to. Include only countries where the story is clearly about that place (politics, events, people, conflict, economy there). Output nothing else—only a JSON array of strings, e.g. ["Ukraine", "Russia"] or ["Iran"]. If the article is not clearly about any specific country, output []. Use at most 5 countries; prefer the 1–3 most relevant."""

USER_PROMPT_TEMPLATE = """Title: {title}

Summary: {summary}

JSON array of relevant country names:"""


def _call_openai(title: str, summary: str) -> list[str]:
    """Call OpenAI (or compatible) API; return list of country names."""
    if not OPENAI_API_KEY:
        return []
    try:
        import openai
    except ImportError:
        log.warning("openai package not installed; run pip install openai for location inference")
        return []

    client_kw: dict[str, Any] = {"api_key": OPENAI_API_KEY}
    if OPENAI_BASE_URL:
        client_kw["base_url"] = OPENAI_BASE_URL
    client = openai.OpenAI(**client_kw)

    user_content = USER_PROMPT_TEMPLATE.format(
        title=(title or "")[:500],
        summary=(summary or "")[:800],
    )
    try:
        resp = client.chat.completions.create(
            model=LOCATION_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            max_tokens=150,
            temperature=0,
        )
        text = (resp.choices[0].message.content or "").strip()
        return _parse_country_list(text)
    except Exception as e:
        log.warning("Location inference API call failed: %s", e)
        return []


def _parse_country_list(text: str) -> list[str]:
    """Parse model output into a list of country names."""
    if not text:
        return []
    # Try to find a JSON array in the response
    match = re.search(r"\[[\s\S]*?\]", text)
    if not match:
        return []
    try:
        raw = json.loads(match.group())
        if not isinstance(raw, list):
            return []
        return [str(c).strip() for c in raw if c and isinstance(c, str) and len(str(c).strip()) > 0]
    except json.JSONDecodeError:
        return []


def infer_relevant_countries(story: dict[str, Any]) -> list[str]:
    """
    Return a list of country names the story is relevant to, or empty if unknown/unavailable.
    Uses an LLM when OPENAI_API_KEY is set; otherwise returns [].
    """
    title = (story.get("title") or "").strip()
    summary = (story.get("summary") or "").strip()
    if not title and not summary:
        return []
    return _call_openai(title, summary)
