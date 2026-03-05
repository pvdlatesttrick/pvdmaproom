"""Verified X report adapters via RSS-capable mirrors."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

import feedparser

NITTER_BASE_URL = os.getenv("NITTER_BASE_URL", "https://nitter.net").rstrip("/")
VERIFIED_X_ACCOUNTS = [
    ("x_reutersworld", "ReutersWorld"),
    ("x_bbcbreaking", "BBCBreaking"),
    ("x_ap", "AP"),
    ("x_un", "UN"),
    ("x_africacenter", "AfricaCDC"),
    ("x_thetimes", "thetimes"),
    ("x_politico", "politico"),
    ("x_janesintel", "JanesINTEL"),
    ("x_rand", "RANDCorporation"),
    ("x_amnesty", "amnesty"),
    # War / conflict reporting
    ("x_isw", "thestudyofwar"),
    ("x_liveuamap", "Liveuamap"),
    # Think tanks – politics / geopolitics
    ("x_carnegie", "CarnegieEndow"),
    ("x_hudson", "HudsonInstitute"),
    # Major news foreign correspondents & top reporters
    ("x_barakravid", "BarakRavid"),      # Axios/WSJ, Israel & Middle East
    ("x_clarissaward", "clarissaward"),  # CNN chief intl correspondent
    ("x_richardengel", "RichardEngel"),  # NBC chief foreign correspondent
    ("x_lynsaddler", "lynsaddler"),      # BBC world affairs
    ("x_nickpatonwalsh", "nickpatonwalsh"),  # CNN intl security
    ("x_borzsandor", "borzsandor"),      # Reuters
    ("x_ianbremmer", "ianbremmer"),      # Eurasia Group / global politics
    # Regional / Middle East – social-first
    ("x_rudaw", "RudawEnglish"),         # Rudaw English (Kurdistan, Iraq, ME)
    ("x_middleeasteye", "MiddleEastEye"),  # Middle East Eye
    ("x_kurdistan24", "Kurdistan24"),    # Kurdistan 24
    ("x_visegrad24", "Visegrad24"),      # Visegrad 24 — conflict video reporting
]


def fetch_verified_x_reports() -> list[dict[str, Any]]:
    """
    Fetch X posts from curated high-trust accounts.
    Uses RSS mirrors because X API credentials are not required.
    """
    stories: list[dict[str, Any]] = []
    for source, handle in VERIFIED_X_ACCOUNTS:
        feed_url = f"{NITTER_BASE_URL}/{handle}/rss"
        parsed = feedparser.parse(feed_url)
        for entry in parsed.entries[:20]:
            stories.append(_normalize_entry(source, handle, entry))
    return stories


def _normalize_entry(source: str, handle: str, entry: Any) -> dict[str, Any]:
    title = str(entry.get("title", "")).strip()
    summary = str(entry.get("summary", "")).strip()
    url = str(entry.get("link", "")).strip()
    published = (
        str(entry.get("published", "")).strip()
        or str(entry.get("updated", "")).strip()
        or datetime.now(timezone.utc).isoformat()
    )
    # Extract video/media URL from RSS enclosures or media content
    related_video_url = None
    for enc in getattr(entry, "enclosures", []):
        enc_url = getattr(enc, "url", None) or enc.get("url", "")
        if enc_url:
            related_video_url = enc_url
            break
    if not related_video_url:
        media_content = getattr(entry, "media_content", [])
        if media_content:
            first = media_content[0]
            related_video_url = getattr(first, "url", None) or (first.get("url") if isinstance(first, dict) else None)
    # Fallback: if the tweet URL itself is an x.com/status link, use it as the video embed
    if not related_video_url and "/status/" in url:
        related_video_url = url

    return {
        "source": source,
        "title": title or f"X report from @{handle}",
        "url": url,
        "summary": summary,
        "published_at": published,
        "related_video_url": related_video_url,
    }

