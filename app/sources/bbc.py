"""BBC RSS source adapter."""

from __future__ import annotations

from typing import Any

import feedparser

BBC_WORLD_RSS = "https://feeds.bbci.co.uk/news/world/rss.xml"


def fetch_bbc_world() -> list[dict[str, Any]]:
    """Fetch BBC World RSS stories in a normalized shape."""
    feed = feedparser.parse(BBC_WORLD_RSS)
    stories: list[dict[str, Any]] = []

    for entry in feed.entries:
        stories.append(
            {
                "source": "bbc",
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", "").strip(),
                "summary": entry.get("summary", "").strip(),
                "published_at": entry.get("published", "").strip(),
            }
        )

    return stories

