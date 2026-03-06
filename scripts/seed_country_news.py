#!/usr/bin/env python3
"""
Seed or update data/country_news/seed.json so every country has at least one entry.

Run from project root:
  python scripts/seed_country_news.py

This creates or merges into app/data/country_news/seed.json. Existing entries are kept;
missing countries get one generic placeholder. Edit seed.json by hand to add real headlines.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Project root = parent of scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "app" / "data" / "country_news"
SEED_PATH = DATA_DIR / "seed.json"
CENTROIDS_PATH = DATA_DIR / "centroids.json"


def get_all_iso2() -> list[str]:
    try:
        import pycountry
        return [c.alpha_2 for c in pycountry.countries if c.alpha_2]
    except ImportError:
        # Fallback: minimal set
        return [
            "AF", "AL", "DZ", "AR", "AM", "AU", "AT", "AZ", "BH", "BD", "BY", "BE", "BJ", "BO", "BA",
            "BW", "BR", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO",
            "KM", "CG", "CD", "CR", "CI", "HR", "CU", "CY", "CZ", "DK", "DJ", "DO", "EC", "EG", "SV",
            "GQ", "ER", "EE", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GR", "GT", "GN",
            "GW", "GY", "HT", "HN", "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IL", "IT", "JM", "JP",
            "JO", "KZ", "KE", "KW", "KG", "LA", "LV", "LB", "LS", "LR", "LY", "LT", "LU", "MG", "MW",
            "MY", "MV", "ML", "MT", "MR", "MU", "MX", "MD", "MN", "ME", "MA", "MZ", "MM", "NA", "NP",
            "NL", "NZ", "NI", "NE", "NG", "KP", "MK", "NO", "OM", "PK", "PS", "PA", "PG", "PY", "PE",
            "PH", "PL", "PT", "PR", "QA", "RO", "RU", "RW", "SA", "SN", "RS", "SG", "SK", "SI", "SO",
            "ZA", "KR", "SS", "ES", "LK", "SD", "SR", "SZ", "SE", "CH", "SY", "TW", "TJ", "TZ", "TH",
            "TL", "TG", "TN", "TR", "TM", "UG", "UA", "AE", "GB", "US", "UY", "UZ", "VE", "VN", "YE",
            "ZM", "ZW",
        ]


def load_centroids() -> dict[str, list[float]]:
    if not CENTROIDS_PATH.exists():
        return {}
    try:
        with CENTROIDS_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def placeholder_entry(iso2: str, name: str) -> dict:
    entry = {
        "title": f"Overview: {name}",
        "summary": "General overview and key facts. Replace with real headlines by editing data/country_news/seed.json or use Admin → Seed.",
        "source_url": f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}",
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "source": "Seed",
        "topic": "geopolitics",
    }
    centroids = load_centroids()
    if iso2 in centroids and isinstance(centroids[iso2], (list, tuple)) and len(centroids[iso2]) >= 2:
        entry["lat"] = float(centroids[iso2][0])
        entry["lon"] = float(centroids[iso2][1])
    return entry


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Load existing seed
    existing: dict[str, list] = {}
    if SEED_PATH.exists():
        try:
            with SEED_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
            existing = data.get("countries") if isinstance(data, dict) else {}
            if not isinstance(existing, dict):
                existing = {}
        except Exception as e:
            print(f"Warning: could not read {SEED_PATH}: {e}", file=sys.stderr)

    try:
        import pycountry
        countries = list(pycountry.countries)
    except ImportError:
        countries = []
        name_by_iso = {}

    added = 0
    for iso2 in get_all_iso2():
        if iso2 in existing and existing[iso2]:
            continue
        name = iso2
        if countries:
            c = next((x for x in countries if x.alpha_2 == iso2), None)
            if c:
                name = c.name or iso2
        existing[iso2] = [placeholder_entry(iso2, name)]
        added += 1

    out = {"countries": existing}
    with SEED_PATH.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print(f"Wrote {SEED_PATH}: {len(existing)} countries, {added} new placeholders.")
    print("Edit app/data/country_news/seed.json to add real headlines per country.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
