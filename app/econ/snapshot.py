"""
Unified economic snapshot for a country: World Bank (primary) + IMF WEO (supplementary) + OECD (optional).
Replaces reliance on The Economist / paywalled dashboards for country-level macro data.
Data sources: World Bank, IMF WEO, OECD (where available). Modular so a licensed API can be swapped in later.
"""

from __future__ import annotations

import logging
from typing import Any

from app.econ.world_bank import get_world_bank_snapshot
from app.econ.imf_weo import get_imf_snapshot
from app.econ.oecd import get_oecd_enrichment, OECD_ISO3

log = logging.getLogger(__name__)


# Fallback when pycountry is unavailable or name not found (common names only).
_COUNTRY_NAME_TO_ISO3: dict[str, str] = {
    "united states": "USA", "united states of america": "USA", "usa": "USA",
    "united kingdom": "GBR", "great britain": "GBR", "uk": "GBR",
    "germany": "DEU", "france": "FRA", "japan": "JPN", "china": "CHN",
    "brazil": "BRA", "india": "IND", "canada": "CAN", "australia": "AUS",
    "russia": "RUS", "italy": "ITA", "spain": "ESP", "south korea": "KOR",
    "mexico": "MEX", "indonesia": "IDN", "netherlands": "NLD", "turkey": "TUR",
    "switzerland": "CHE", "poland": "POL", "belgium": "BEL", "sweden": "SWE",
    "argentina": "ARG", "austria": "AUT", "norway": "NOR", "israel": "ISR",
    "south africa": "ZAF", "egypt": "EGY", "thailand": "THA", "nigeria": "NGA",
    "paraguay": "PRY", "uruguay": "URY", "chile": "CHL", "colombia": "COL",
    "peru": "PER", "ecuador": "ECU", "venezuela": "VEN", "myanmar": "MMR",
}


def _country_name_to_iso3(country_name: str) -> str | None:
    """Resolve country name to ISO 3166-1 alpha-3. Returns None if not found."""
    s = (country_name or "").strip()
    if not s:
        return None
    if len(s) == 3 and s.isalpha():
        return s.upper()
    if len(s) == 2 and s.isalpha():
        try:
            import pycountry
            c = pycountry.countries.get(alpha_2=s.upper())
            return c.alpha_3 if c else None
        except Exception:
            pass
    key = s.lower().replace(",", "").strip()
    if key in _COUNTRY_NAME_TO_ISO3:
        return _COUNTRY_NAME_TO_ISO3[key]
    try:
        import pycountry
        c = pycountry.countries.get(name=s)
        if not c:
            matches = pycountry.countries.search_fuzzy(s)
            c = matches[0] if matches else None
        return c.alpha_3 if c else None
    except Exception:
        return None


def get_country_econ_snapshot(iso3: str | None, country_name: str | None) -> dict[str, Any]:
    """
    Build a single economic snapshot for the side panel / popup.
    - Baseline from World Bank (required).
    - Overlay IMF WEO where available (supplementary); overlap fields kept separate (e.g. imf_gdp_growth_pct).
    - If country is OECD, merge OECD enrichment.
    Returns a small dict with only fields that are present; sources listed in "sources".
    """
    iso = (iso3 or "").strip().upper() if iso3 else None
    if not iso and country_name:
        iso = _country_name_to_iso3(country_name)
    if not iso:
        return {}

    # 1) World Bank baseline
    wb = get_world_bank_snapshot(iso)
    result: dict[str, Any] = {}
    sources: list[str] = []

    if wb:
        result["gdp_current_usd"] = wb.get("gdp_current_usd")
        result["gdp_per_capita_usd"] = wb.get("gdp_per_capita_usd")
        result["gdp_growth_pct"] = wb.get("gdp_growth_pct")
        result["inflation_pct"] = wb.get("inflation_cpi_pct")
        result["unemployment_pct"] = wb.get("unemployment_pct")
        result["year"] = wb.get("year")
        sources.append("World Bank")

    # 2) IMF WEO supplementary
    imf_input = iso if iso else (country_name or "")
    imf = get_imf_snapshot(imf_input) if imf_input else {}
    if imf:
        if imf.get("gdp_growth_pct") is not None:
            result["imf_gdp_growth_pct"] = imf["gdp_growth_pct"]
        if imf.get("inflation_pct") is not None:
            result["imf_inflation_pct"] = imf["inflation_pct"]
        if imf.get("debt_pct_gdp") is not None:
            result["debt_pct_gdp"] = imf["debt_pct_gdp"]
        if imf.get("fiscal_balance_pct_gdp") is not None:
            result["fiscal_balance_pct_gdp"] = imf["fiscal_balance_pct_gdp"]
        if imf.get("year") and not result.get("year"):
            result["year"] = imf["year"]
        if "IMF WEO" not in sources:
            sources.append("IMF WEO")

    # 3) OECD enrichment (members only)
    if iso in OECD_ISO3:
        oecd = get_oecd_enrichment(iso)
        if oecd:
            if oecd.get("unemployment_detail_pct") is not None:
                result["oecd_unemployment_pct"] = oecd["unemployment_detail_pct"]
            if "OECD" not in sources:
                sources.append("OECD")

    # Drop None values for a compact response
    result = {k: v for k, v in result.items() if v is not None}
    if sources:
        result["sources"] = sources
    return result
