"""
PVD-style relevance/importance scoring for sidebar ordering.
Higher score = more important; used to sort "Coverage from all sources" and similar lists.
"""

from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any


def _parse_published_ts(published_at: str | None) -> float:
    """Return Unix timestamp for published_at, or 0 if unparseable."""
    if not (published_at and str(published_at).strip()):
        return 0.0
    s = str(published_at).strip()
    try:
        if "T" in s and "-" in s:
            dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        else:
            dt = parsedate_to_datetime(s)
        return dt.timestamp() if dt.tzinfo else dt.replace(tzinfo=timezone.utc).timestamp()
    except Exception:
        return 0.0


def compute_age_hours(published_at: str | None) -> float:
    """Hours since published; 0 if unparseable."""
    ts = _parse_published_ts(published_at)
    if ts <= 0:
        return 9999.0
    return (datetime.now(timezone.utc).timestamp() - ts) / 3600.0


def score_story_pvd(story: dict[str, Any]) -> float:
    """
    Return a numeric PVD-style importance score for this story.
    Higher = more important / more relevant for sidebar ordering.
    """
    score = 0.0
    topic = (story.get("topic") or "").strip().lower()
    if topic == "geopolitics":
        score += 5.0
    elif topic == "economics":
        score += 4.0
    elif topic == "conflicts":
        score += 5.0
    elif topic == "sports":
        score += 2.0
    elif topic == "history":
        score += 3.0
    else:
        score += 1.0

    text = ((story.get("title") or "") + " " + (story.get("summary") or "")).lower()

    if any(
        k in text
        for k in [
            "sanctions",
            "treaty",
            "ceasefire",
            "offensive",
            "escalation",
            "strike",
            "mobilization",
            "nuclear",
        ]
    ):
        score += 2.0

    if any(
        k in text
        for k in [
            "inflation",
            "interest rate",
            "central bank",
            "fed ",
            "ecb",
            "stimulus",
            "austerity",
            "recession",
            "deficit",
            "debt ceiling",
            "fiscal",
            "gdp",
            "trade deficit",
            "tariff",
        ]
    ):
        score += 2.0

    if any(
        k in text
        for k in [
            "constitution",
            "constitutional",
            "supreme court",
            "election",
            "referendum",
            "coalition",
            "coup",
            "impeachment",
        ]
    ):
        score += 2.0

    if topic == "sports":
        if any(
            k in text
            for k in [
                "depth chart",
                "tidbits",
                "team tidbits",
                "beat writer",
                "small note",
                "minor injury",
                "practice notes",
            ]
        ):
            score -= 1.5
        if any(
            k in text
            for k in [
                "rumors",
                "trade rumor",
                "mock draft",
                "power rankings",
            ]
        ):
            score -= 0.5

    if any(
        k in text
        for k in [
            "fashion",
            "celebrity",
            "wedding",
            "viral video",
            "social media reacts",
        ]
    ):
        score -= 1.0

    age_hours = compute_age_hours(story.get("published_at"))
    if age_hours <= 6:
        score += 1.0
    elif age_hours <= 24:
        score += 0.5

    source = (story.get("source") or "").lower()
    if any(
        k in source
        for k in [
            "economist",
            "wall-street-journal",
            "wsj",
            "hudson",
            "aei",
            "dispatch",
        ]
    ):
        score += 0.7
    if any(
        k in source
        for k in [
            "washington-post",
            "nytimes",
            "financial-times",
        ]
    ):
        score += 0.3

    return float(score)
