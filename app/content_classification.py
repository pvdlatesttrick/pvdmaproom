"""
Content type classification (reporting / analysis / opinion / speculation) for map filtering.
Map shows only reporting and factual coverage by default; opinion/speculation allowed only from
The Economist and The Dispatch.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from app.ai_summary import SUMMARY_MODEL

log = logging.getLogger(__name__)

CONTENT_TYPES = frozenset({"reporting", "analysis", "opinion", "speculation"})

CONTENT_TYPE_SYSTEM = """You are a media literacy classifier. Your job is to label one article as 'reporting', 'analysis', 'opinion', or 'speculation'.

Definitions:
- reporting: straightforward presentation of verified facts about events (who/what/when/where/why), neutral tone, minimal interpretation.
- analysis: interprets and explains events using facts and data; still grounded in evidence, but focuses on meaning and implications.
- opinion: expresses a personal or editorial viewpoint, often using persuasive language, first person, or a clear argument about what should be done.
- speculation: focuses mainly on unconfirmed possibilities or predictions (what might happen) rather than established facts; heavy use of words like 'might', 'could', 'likely', 'rumor', 'unconfirmed', without solid sourcing.

Rules:
- If an article is primarily factual reporting with some minor interpretation, label it 'reporting'.
- If it is primarily about explaining what the facts mean, without pushing a personal agenda, label it 'analysis'.
- If it is clearly taking a side or arguing a thesis, label it 'opinion'.
- If it is mostly about rumors, unconfirmed claims, or predictions, label it 'speculation'.
- Output ONLY one word: reporting, analysis, opinion, or speculation."""

# URL path segments that strongly suggest opinion section
OPINION_PATH_PATTERN = re.compile(
    r"/?(?:opinion|editorial|editorials|views|op-?ed|comment|commentary|blog)/",
    re.I,
)

# Title/summary phrases that suggest speculation (optional heuristic)
SPECULATION_PHRASES = re.compile(
    r"\b(could\s+\w+\s+happen\?|will\s+\w+\s+\?|what\s+if\s+|is\s+.\s+about\s+to\s+|"
    r"rumors?:\s*|unconfirmed\s+|sources?\s+say\s+.\s+may\s+|might\s+be\s+about\s+to)\b",
    re.I,
)


def _heuristic_content_type(story: dict[str, Any]) -> str | None:
    """Return content_type from URL/title heuristics, or None to use LLM."""
    url = (story.get("url") or "").strip()
    if OPINION_PATH_PATTERN.search(url):
        return "opinion"
    title = (story.get("title") or "").strip()
    summary = (story.get("summary") or "").strip()
    text = f"{title} {summary}"
    if SPECULATION_PHRASES.search(text):
        return "speculation"
    return None


def classify_content_type(story: dict[str, Any], model_client: Any) -> str:
    """
    Classify this story as 'reporting', 'analysis', 'opinion', or 'speculation'.
    Uses optional URL/title heuristics first; otherwise calls the LLM.
    """
    heuristic = _heuristic_content_type(story)
    if heuristic is not None:
        return heuristic

    if not model_client:
        return "reporting"

    try:
        user_content = (
            f"Source: {story.get('source', '')}\n\n"
            f"Title: {story.get('title', '')}\n\n"
            f"Summary: {story.get('summary', '')}"
        )
        resp = model_client.chat.completions.create(
            model=SUMMARY_MODEL,
            messages=[
                {"role": "system", "content": CONTENT_TYPE_SYSTEM},
                {"role": "user", "content": user_content[:8000]},
            ],
            max_tokens=10,
            temperature=0,
        )
        label = (resp.choices[0].message.content or "").strip().lower()
        label = label.split()[0] if label else ""
        if label in CONTENT_TYPES:
            return label
    except Exception as e:
        log.warning("Content type classification failed: %s", e)
    return "reporting"


def should_include_story_on_map(story: dict[str, Any]) -> bool:
    """
    Return True if this story should be indexed for map display.
    - The Economist and The Dispatch: allow reporting, analysis, opinion, speculation.
    - All other sources: allow only reporting and analysis; exclude opinion and speculation.
    """
    source = (story.get("source") or "").lower()
    content_type = (story.get("content_type") or "reporting").lower().strip()

    is_economist = "economist" in source
    is_dispatch = "dispatch" in source

    if is_economist or is_dispatch:
        return True

    if content_type in {"opinion", "speculation"}:
        return False

    return True
