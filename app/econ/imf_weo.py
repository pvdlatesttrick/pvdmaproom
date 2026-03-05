"""
IMF World Economic Outlook (WEO) – supplementary macro data.
Uses free IMF data sources where available. If no public API is reachable,
returns {} so the app still shows World Bank data only.
Optional: plug in an Apify or other WEO wrapper by replacing the fetch logic.
"""

from __future__ import annotations

import logging
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

log = logging.getLogger(__name__)

# IMF Data API (SDMX/JSON). WEO by country; structure may vary.
# Fallback: return {} so World Bank remains the baseline.
REQUEST_TIMEOUT = 10
USER_AGENT = "pvdmaproom/1.0 (news map; economic data)"


def get_imf_snapshot(country_name_or_iso: str) -> dict[str, Any]:
    """
    Fetch latest WEO-style indicators if available: real GDP growth, inflation,
    government debt (% GDP), fiscal balance (% GDP). Returns compact dict with
    gdp_growth_pct, inflation_pct, debt_pct_gdp, fiscal_balance_pct_gdp, year, source.
    Supplementary: on failure return {} so caller can still use World Bank only.
    """
    # IMF public SDMX endpoints require dataset/country/indicator codes and can be brittle.
    # Try a known pattern; if it fails, return {} and rely on World Bank.
    result: dict[str, Any] = {}
    try:
        # Example: WEO dataset, country code, growth indicator. Adjust codes as per IMF docs.
        # Many IMF endpoints use ISO2 or IMF-specific codes. Here we try and catch.
        _try_imf_weo_fetch(country_name_or_iso, result)
    except Exception as e:
        log.debug("IMF WEO fetch failed for %s: %s", country_name_or_iso[:30], e)
    if result:
        result.setdefault("source", "IMF WEO")
    return result


def _try_imf_weo_fetch(country_name_or_iso: str, out: dict[str, Any]) -> None:
    """Attempt to fill out with WEO data. Leaves out unchanged on failure."""
    iso2 = _to_imf_country_code(country_name_or_iso)
    if not iso2:
        return
    url = (
        "https://www.imf.org/external/datamapper/api/v1/weo?"
        + urllib.parse.urlencode({"country": iso2})
    )
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            raw = resp.read().decode()
    except (urllib.error.URLError, OSError, ValueError):
        return
    try:
        import json
        data = json.loads(raw)
    except Exception:
        return
    if not isinstance(data, dict):
        return
    weo = data.get("weo") or data.get(iso2) or data
    if not isinstance(weo, dict):
        return
    for key, attr in (
        ("NGDP_RPCH", "gdp_growth_pct"),
        ("PCPIPCH", "inflation_pct"),
        ("GGXWDG_NGDP", "debt_pct_gdp"),
        ("GGXOBL_NGDP", "fiscal_balance_pct_gdp"),
    ):
        series = weo.get(key)
        if isinstance(series, dict):
            val, year = _latest_value(series)
            if val is not None:
                out[attr] = val
                if year and (out.get("year") is None or (year > out.get("year", ""))):
                    out["year"] = year
    if not out.get("year") and weo:
        for k, v in weo.items():
            if isinstance(v, dict) and v:
                _, year = _latest_value(v)
                if year:
                    out.setdefault("year", year)
                    break


def _latest_value(series: dict[str, Any]) -> tuple[float | None, str | None]:
    """From a dict of year -> value, return (value, year) for the latest year."""
    if not series:
        return None, None
    years = [k for k in series if isinstance(k, str) and k.isdigit()]
    if not years:
        return None, None
    year = max(years, key=int)
    try:
        return float(series[year]), year
    except (TypeError, ValueError):
        return None, year


def _to_imf_country_code(name_or_iso: str) -> str | None:
    """Map country name or ISO code to 2-letter code used by IMF (often ISO2)."""
    s = (name_or_iso or "").strip()
    if not s:
        return None
    if len(s) == 2 and s.isalpha():
        return s.upper()
    if len(s) == 3 and s.isalpha():
        # ISO3 -> ISO2 via simple mapping for major economies (IMF often uses ISO2)
        iso3_to_2 = {
            "USA": "US", "GBR": "GB", "DEU": "DE", "FRA": "FR", "JPN": "JP", "CHN": "CN",
            "IND": "IN", "BRA": "BR", "CAN": "CA", "AUS": "AU", "ITA": "IT", "ESP": "ES",
            "KOR": "KR", "MEX": "MX", "RUS": "RU", "ZAF": "ZA", "NLD": "NL", "CHE": "CH",
        }
        return iso3_to_2.get(s.upper())
    # Name -> ISO2 via pycountry if available
    try:
        import pycountry
        c = pycountry.countries.get(name=s) or pycountry.countries.search_fuzzy(s)[0]
        return c.alpha_2 if c else None
    except Exception:
        return None
