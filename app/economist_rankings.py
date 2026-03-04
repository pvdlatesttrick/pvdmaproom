"""
Economist-style rankings (Democracy Index, etc.) for country panel.

Data sources are configurable via env; update whenever The Economist publishes
by re-running update_rankings() (e.g. with ingest or a cron job).
See: https://www.economist.com/news/2009/05/29/rankings-calendar
"""

from __future__ import annotations

import csv
import json
import os
from typing import Any
from urllib.request import urlopen

from app.factbook import normalize_country_name

# Indicator keys and display names (aligned with Economist rankings calendar)
RANKING_INDICATORS = {
    "democracy_index": "Democracy Index (EIU)",
    "big_mac_index": "Big Mac Index",
    "cost_of_living": "Cost of Living",
    "quality_of_life": "Quality of Life",
}

# Optional: URL to a CSV with columns: country, score [, rank, year]
# CSV: country name, numeric score; rank is computed from score order if missing
ECONOMIST_RANKINGS_DEMOCRACY_URL = os.getenv(
    "ECONOMIST_RANKINGS_DEMOCRACY_URL",
    "",
).strip()

# Optional: URL to JSON array of { "country": "...", "score": n, "rank": n?, "year": "2024"? }
ECONOMIST_RANKINGS_DEMOCRACY_JSON_URL = os.getenv(
    "ECONOMIST_RANKINGS_DEMOCRACY_JSON_URL",
    "",
).strip()


def _parse_democracy_csv(content: str) -> list[dict[str, Any]]:
    """Parse CSV with country and score (and optional rank/year)."""
    rows: list[dict[str, Any]] = []
    try:
        reader = csv.DictReader(content.strip().splitlines())
        for row in reader:
            country = (row.get("country") or row.get("name") or row.get("Country") or "").strip()
            score_s = (row.get("score") or row.get("Score") or row.get("eiu") or "").strip()
            rank_s = (row.get("rank") or row.get("Rank") or "").strip()
            year_s = (row.get("year") or row.get("Year") or "").strip()
            if not country or not score_s:
                continue
            try:
                score = float(score_s.replace(",", "."))
            except ValueError:
                continue
            rank = int(rank_s) if rank_s and rank_s.isdigit() else None
            rows.append({
                "country": country,
                "score": round(score, 2),
                "rank": rank,
                "year": year_s or None,
            })
    except Exception:
        pass
    if rows and not any(r.get("rank") for r in rows):
        rows.sort(key=lambda r: (r["score"], r["country"]), reverse=True)
        for i, r in enumerate(rows, 1):
            r["rank"] = i
    return rows


def _parse_democracy_json(content: str) -> list[dict[str, Any]]:
    """Parse JSON array of { country, score [, rank, year ] }."""
    out: list[dict[str, Any]] = []
    try:
        data = json.loads(content)
        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    continue
                country = (item.get("country") or item.get("name") or "").strip()
                score = item.get("score")
                if not country or score is None:
                    continue
                try:
                    score = float(score)
                except (TypeError, ValueError):
                    continue
                rank = item.get("rank")
                if rank is not None:
                    try:
                        rank = int(rank)
                    except (TypeError, ValueError):
                        rank = None
                out.append({
                    "country": country,
                    "score": round(score, 2),
                    "rank": rank,
                    "year": item.get("year"),
                })
        if out and not any(r.get("rank") for r in out):
            out.sort(key=lambda r: (r["score"], r["country"]), reverse=True)
            for i, r in enumerate(out, 1):
                r["rank"] = i
    except Exception:
        pass
    return out


def fetch_democracy_index() -> list[dict[str, Any]]:
    """Fetch Democracy Index data from configured URL (CSV or JSON)."""
    if ECONOMIST_RANKINGS_DEMOCRACY_JSON_URL:
        try:
            with urlopen(ECONOMIST_RANKINGS_DEMOCRACY_JSON_URL, timeout=15) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            return _parse_democracy_json(raw)
        except Exception:
            pass
    if ECONOMIST_RANKINGS_DEMOCRACY_URL:
        try:
            with urlopen(ECONOMIST_RANKINGS_DEMOCRACY_URL, timeout=15) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            return _parse_democracy_csv(raw)
        except Exception:
            pass
    return []


def load_bundled_rankings() -> list[dict[str, Any]]:
    """Load a small bundled snapshot if no URL is set (sample for display)."""
    _bundled = [
        {"country": "Norway", "score": 9.81, "rank": 1, "year": "2024"},
        {"country": "New Zealand", "score": 9.61, "rank": 2, "year": "2024"},
        {"country": "Iceland", "score": 9.45, "rank": 3, "year": "2024"},
        {"country": "Sweden", "score": 9.39, "rank": 4, "year": "2024"},
        {"country": "Finland", "score": 9.30, "rank": 5, "year": "2024"},
        {"country": "Denmark", "score": 9.28, "rank": 6, "year": "2024"},
        {"country": "Ireland", "score": 9.19, "rank": 7, "year": "2024"},
        {"country": "Switzerland", "score": 9.14, "rank": 8, "year": "2024"},
        {"country": "Netherlands", "score": 9.00, "rank": 9, "year": "2024"},
        {"country": "Taiwan", "score": 8.92, "rank": 10, "year": "2024"},
        {"country": "United Kingdom", "score": 8.28, "rank": 18, "year": "2024"},
        {"country": "United States of America", "score": 7.85, "rank": 23, "year": "2024"},
        {"country": "France", "score": 7.79, "rank": 24, "year": "2024"},
        {"country": "Germany", "score": 8.52, "rank": 15, "year": "2024"},
        {"country": "Japan", "score": 7.80, "rank": 25, "year": "2024"},
        {"country": "South Korea", "score": 8.00, "rank": 22, "year": "2024"},
        {"country": "India", "score": 6.57, "rank": 41, "year": "2024"},
        {"country": "Brazil", "score": 6.78, "rank": 36, "year": "2024"},
        {"country": "South Africa", "score": 7.05, "rank": 31, "year": "2024"},
        {"country": "Argentina", "score": 6.63, "rank": 40, "year": "2024"},
    ]
    return _bundled


def get_democracy_index_entries() -> list[dict[str, Any]]:
    """Return Democracy Index entries (from URL or bundled)."""
    entries = fetch_democracy_index()
    if not entries:
        entries = load_bundled_rankings()
    return entries


def build_rankings_for_db() -> list[tuple[str, str, int | None, float | None, str | None]]:
    """
    Build list of (country_name_normalized, indicator_key, rank, score, year) for DB.
    Uses Democracy Index only for now; extend for Big Mac etc. when URLs are added.
    """
    rows: list[tuple[str, str, int | None, float | None, str | None]] = []  # (country, indicator, rank, score, year)
    entries = get_democracy_index_entries()
    for e in entries:
        country = (e.get("country") or "").strip()
        if not country:
            continue
        key = normalize_country_name(country)
        if not key:
            continue
        rank = e.get("rank")
        score = e.get("score")
        year = e.get("year")
        if isinstance(year, (int, float)):
            year = str(int(year))
        rows.append((key, "democracy_index", rank, score, year))
    return rows
