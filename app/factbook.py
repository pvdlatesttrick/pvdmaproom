"""CIA World Factbook helpers (top fields only)."""

from __future__ import annotations

import json
import os
import re
from typing import Any
from urllib.request import urlopen

FACTBOOK_URL = (
    "https://raw.githubusercontent.com/iancoleman/"
    "cia_world_factbook_api/master/data/factbook.json"
)


def normalize_country_name(name: str) -> str:
    lowered = (name or "").strip().lower()
    lowered = lowered.replace("&", " and ")
    lowered = re.sub(r"\bu\.s\.\b", "united states", lowered)
    lowered = re.sub(r"\bus\b", "united states", lowered)
    lowered = re.sub(r"[^a-z0-9 ]+", " ", lowered)
    return re.sub(r"\s+", " ", lowered).strip()


def _format_number(value: Any) -> str | None:
    if not isinstance(value, (int, float)):
        return None
    return f"{value:,.0f}"


def _extract_latest_gdp_ppp(country_data: dict[str, Any]) -> str | None:
    annual = (
        country_data.get("economy", {})
        .get("gdp", {})
        .get("purchasing_power_parity", {})
        .get("annual_values", [])
    )
    if not annual:
        return None
    value = annual[0].get("value")
    date = annual[0].get("date")
    formatted = _format_number(value)
    if not formatted:
        return None
    if date:
        return f"${formatted} ({date})"
    return f"${formatted}"


def _extract_area_total(country_data: dict[str, Any]) -> str | None:
    area = country_data.get("geography", {}).get("area", {}).get("total", {})
    value = _format_number(area.get("value"))
    units = area.get("units")
    if not value:
        return None
    return f"{value} {units or ''}".strip()


def _extract_population(country_data: dict[str, Any]) -> str | None:
    pop = country_data.get("people", {}).get("population", {})
    value = _format_number(pop.get("total"))
    date = pop.get("date")
    if not value:
        return None
    if date:
        return f"{value} ({date})"
    return value


def _extract_capital(country_data: dict[str, Any]) -> str | None:
    return country_data.get("government", {}).get("capital", {}).get("name")


def _extract_government_type(country_data: dict[str, Any]) -> str | None:
    return country_data.get("government", {}).get("government_type")


def _extract_economic_rank(country_data: dict[str, Any]) -> str | None:
    gdp_ppp = (
        country_data.get("economy", {})
        .get("gdp", {})
        .get("purchasing_power_parity", {})
    )
    rank = gdp_ppp.get("global_rank")
    if isinstance(rank, int):
        return f"#{rank} GDP (PPP) size"

    per_capita = (
        country_data.get("economy", {})
        .get("gdp", {})
        .get("per_capita_purchasing_power_parity", {})
    )
    per_capita_rank = per_capita.get("global_rank")
    if isinstance(per_capita_rank, int):
        return f"#{per_capita_rank} GDP (PPP) per capita"
    return None


def load_factbook() -> dict[str, Any]:
    """Load raw Factbook payload from the configured source."""
    source_url = os.getenv("CIA_FACTBOOK_URL", FACTBOOK_URL).strip() or FACTBOOK_URL
    with urlopen(source_url, timeout=30) as resp:
        return json.load(resp)


def build_country_facts_index(payload: dict[str, Any]) -> dict[str, dict[str, str | None]]:
    """Build normalized-name index of top CIA fact fields."""
    countries = payload.get("countries", {})
    index: dict[str, dict[str, str | None]] = {}
    for country_obj in countries.values():
        data = country_obj.get("data", {})
        country_name = str(data.get("name", "")).strip()
        if not country_name:
            continue
        key = normalize_country_name(country_name)
        if not key:
            continue
        index[key] = {
            "country_name": country_name,
            "capital": _extract_capital(data),
            "population": _extract_population(data),
            "gdp_ppp": _extract_latest_gdp_ppp(data),
            "area_total": _extract_area_total(data),
            "government_type": _extract_government_type(data),
            "economist_economic_rank": _extract_economic_rank(data),
        }
    return index


def lookup_country_fact(
    facts_index: dict[str, dict[str, str | None]], country_name: str | None
) -> dict[str, str | None] | None:
    """Look up one country fact entry by fuzzy-normalized country name."""
    key = normalize_country_name(country_name or "")
    if not key:
        return None
    return facts_index.get(key)

