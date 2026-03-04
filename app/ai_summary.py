"""
Generate AI summaries with broader context for a country or a news story.
Uses the same OpenAI-compatible API as location inference (OPENAI_API_KEY, OPENAI_BASE_URL).
"""

from __future__ import annotations

import logging
import os
from typing import Any

log = logging.getLogger(__name__)

SUMMARY_MODEL = os.getenv("SUMMARY_MODEL", os.getenv("LOCATION_MODEL", "gpt-4o-mini")).strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip()

COUNTRY_SYSTEM = """You are a concise analyst. Given a country name and optional basic facts (capital, population, etc.), write a short summary (2–4 sentences) that gives broader context: current relevance in the news, key geopolitical or economic themes, and why the country matters right now. Use neutral, factual language. Output only the summary text, no headings or bullet points."""

STORY_SYSTEM = """You are a concise analyst. Given a news story's title and summary, write a short summary (2–4 sentences) that: (1) briefly states what the story is about, and (2) adds broader context—why it matters, background, or how it fits into larger developments. Use neutral, factual language. If the story is about a specific country or region, mention that. Output only the summary text, no headings or bullet points."""

TITLE_SYSTEM = """You write short headlines for news articles and social posts. Given the article or post content (and optional URL or raw title), output a single clear headline in sentence case. One line only, no quotes, no period at the end. Do not output a URL or repeat the URL. Maximum about 80 characters. Be specific and factual."""


def _client():
    """Return OpenAI-compatible client or None if not configured."""
    if not OPENAI_API_KEY:
        return None
    try:
        import openai
    except ImportError:
        return None
    kwargs: dict[str, Any] = {"api_key": OPENAI_API_KEY}
    if OPENAI_BASE_URL:
        kwargs["base_url"] = OPENAI_BASE_URL
    return openai.OpenAI(**kwargs)


def summarize_country(country_name: str, facts: dict[str, Any] | None = None) -> str | None:
    """Return an AI-generated summary and broader context for the country, or None if unavailable."""
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
    user_content = f"Country: {country_name.strip()}{facts_text}\n\nWrite the summary:"
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
