"""
AI chatbot for the map: answers questions using ingested articles and think-tank data.
Aligns with the analytical perspective of WSJ, The Economist, Hudson Institute, AEI, The Dispatch.
"""

from __future__ import annotations

import logging
import os
from typing import Any

log = logging.getLogger(__name__)

CHAT_MODEL = os.getenv("CHAT_MODEL", os.getenv("SUMMARY_MODEL", "gpt-4o-mini")).strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip()

# Preferred sources for context and alignment (include more of these in context).
PREFERRED_SOURCES = frozenset({
    "wsj", "economist", "economist_asia", "economist_mea", "economist_graphic_detail",
    "economist_podcast",
    "hudson", "aei", "dispatch",
    "x_hudson", "x_carnegie",
})

SYSTEM_PROMPT = """You are PVD, an analyst answering questions about current events and the world using the map's data. You have access to recent headlines and summaries from news outlets, think tanks, and publications.

Use only the provided "Recent reporting and data" below to inform your answers. Cite which source or region a point comes from when relevant. Give clear insights and opinions.

Your analysis should align with the perspective of outlets such as the Wall Street Journal, The Economist, the Hudson Institute, the American Enterprise Institute, and The Dispatch: fact-based, supportive of free markets and strong institutions, skeptical of government overreach, and attentive to geopolitical and economic risks. Be concise but substantive. If the user asks about a specific country or topic, focus on that; otherwise draw on the most relevant items in the data. If asked who you are, say you are PVD."""


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


def _prioritize_stories_for_chat(stories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Put preferred sources (WSJ, Economist, Hudson, AEI, Dispatch) first, then by date."""
    def key(s: dict[str, Any]) -> tuple[int, str]:
        src = (s.get("source") or "").strip().lower()
        preferred = 0 if src in PREFERRED_SOURCES else 1
        pub = (s.get("published_at") or "")[:20]
        return (preferred, pub)

    return sorted(stories, key=key)


def _build_context_from_stories(stories: list[dict[str, Any]], max_chars: int = 28000) -> str:
    """Turn a list of story dicts (source, title, summary, country, published_at) into a text block for the LLM."""
    lines: list[str] = []
    total = 0
    for s in stories:
        source = (s.get("source") or "").strip()
        title = (s.get("title") or "").strip()
        summary = (s.get("summary") or "").strip()[:800]
        country = (s.get("country") or "").strip()
        pub = (s.get("published_at") or "").strip()
        block = f"[{source}]"
        if country:
            block += f" ({country})"
        if pub:
            block += f" {pub}"
        block += f"\n  {title}\n  {summary}\n"
        if total + len(block) > max_chars:
            break
        lines.append(block)
        total += len(block)
    return "\n".join(lines) if lines else "(No recent articles in the database.)"


def chat(
    user_message: str,
    stories: list[dict[str, Any]],
    map_key: str | None = None,
    country: str | None = None,
) -> str | None:
    """
    Reply to the user using the given stories as context. Returns the assistant reply or None if API unavailable.
    """
    if not (user_message or "").strip():
        return None
    client = _client()
    if not client:
        return None

    prioritized = _prioritize_stories_for_chat(stories)
    context = _build_context_from_stories(prioritized)
    map_note = ""
    if map_key:
        map_note = f"\nCurrent map view: {map_key}."
    if country:
        map_note += f" User may be interested in: {country}."

    user_content = f"Recent reporting and data from the map:\n\n{context}\n\n---\nUser question:{map_note}\n\n{user_message.strip()}"

    try:
        resp = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            max_tokens=1200,
            temperature=0.4,
        )
        text = (resp.choices[0].message.content or "").strip()
        return text if text else None
    except Exception as e:
        log.warning("Chat API call failed: %s", e)
        return None
