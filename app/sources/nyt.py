"""NYT Top Stories source adapter."""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode
from urllib.request import urlopen

NYT_WORLD_ENDPOINT = "https://api.nytimes.com/svc/topstories/v2/world.json"


def fetch_nyt_top_stories(api_key: str) -> list[dict[str, Any]]:
    """Fetch NYT top stories in a normalized shape."""
    url = f"{NYT_WORLD_ENDPOINT}?{urlencode({'api-key': api_key})}"
    with urlopen(url, timeout=20) as resp:
        payload = json.load(resp)

    stories: list[dict[str, Any]] = []
    for item in payload.get("results", []):
        stories.append(
            {
                "source": "nyt",
                "title": str(item.get("title", "")).strip(),
                "url": str(item.get("url", "")).strip(),
                "summary": str(item.get("abstract", "")).strip(),
                "published_at": str(item.get("published_date", "")).strip(),
            }
        )

    return stories

