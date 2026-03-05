"""Fetch The Economist podcast (The Intelligence) episode metadata for chatbot context.
Uses the public RSS feed; we ingest episode titles and descriptions only (no audio)."""

from __future__ import annotations

import logging
import re
from typing import Any

import feedparser

log = logging.getLogger(__name__)

THE_INTELLIGENCE_RSS = "https://feeds.acast.com/public/shows/theintelligencepodcast"
MAX_EPISODES = 50


def _strip_html(text: str) -> str:
    """Remove HTML tags and decode common entities for plain-text summary."""
    if not text:
        return ""
    # Remove tags
    out = re.sub(r"<[^>]+>", " ", text)
    # Decode common entities
    out = out.replace("&apos;", "'").replace("&quot;", '"').replace("&amp;", "&")
    out = out.replace("&lt;", "<").replace("&gt;", ">")
    out = re.sub(r"\s+", " ", out).strip()
    return out[:2000]  # cap length for DB/context


def fetch_economist_podcast() -> list[dict[str, Any]]:
    """Fetch The Intelligence podcast RSS and return episode entries as story-like dicts.
    Episodes have no single country; ingest will assign 'World' for chat context only."""
    stories: list[dict[str, Any]] = []
    try:
        parsed = feedparser.parse(THE_INTELLIGENCE_RSS)
    except Exception as e:
        log.warning("Economist podcast RSS failed: %s", e)
        return stories
    for entry in parsed.entries[:MAX_EPISODES]:
        title = (entry.get("title") or "").strip()
        link = (entry.get("link") or "").strip()
        if not title or not link:
            continue
        summary = (
            entry.get("summary") or entry.get("description") or ""
        )
        if isinstance(summary, str):
            summary = _strip_html(summary)
        else:
            summary = _strip_html(getattr(summary, "value", "") or "")
        published = (
            str(entry.get("published") or entry.get("updated") or entry.get("pubDate") or "")
        ).strip()
        stories.append({
            "source": "economist_podcast",
            "title": title,
            "url": link,
            "summary": summary or title,
            "published_at": published,
        })
    return stories
