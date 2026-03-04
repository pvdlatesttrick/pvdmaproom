"""Country localized/English name helpers."""

from __future__ import annotations

import json
from typing import Any
from urllib.request import urlopen

from app.factbook import normalize_country_name

REST_COUNTRIES_URL = "https://restcountries.com/v3.1/all?fields=name,translations"


def fetch_country_name_index() -> dict[str, dict[str, str]]:
    """Load country name metadata keyed by normalized English name."""
    with urlopen(REST_COUNTRIES_URL, timeout=30) as resp:
        payload = json.load(resp)

    index: dict[str, dict[str, str]] = {}
    for item in payload:
        name = item.get("name", {}) or {}
        english = str(name.get("common", "")).strip()
        if not english:
            continue

        native_name = _pick_native_name(item)
        key = normalize_country_name(english)
        if not key:
            continue
        index[key] = {
            "english_name": english,
            "original_name": native_name or english,
        }
    return index


def _pick_native_name(item: dict[str, Any]) -> str | None:
    """Try native name first; then one translation as original-language label."""
    name = item.get("name", {}) or {}
    native_name_obj = name.get("nativeName", {}) or {}
    for val in native_name_obj.values():
        common = str((val or {}).get("common", "")).strip()
        if common:
            return common

    translations = item.get("translations", {}) or {}
    for val in translations.values():
        common = str((val or {}).get("common", "")).strip()
        if common:
            return common
    return None

