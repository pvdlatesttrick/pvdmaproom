"""
World Bank Indicators API – primary source for per-country macro data.
Docs: https://datahelpdesk.worldbank.org/knowledgebase/articles/898590-country-api-queries
      https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
No authentication required. Free for programmatic use.
"""

from __future__ import annotations

import logging
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

log = logging.getLogger(__name__)

BASE_URL = "https://api.worldbank.org/v2"
REQUEST_TIMEOUT = 12
USER_AGENT = "pvdmaproom/1.0 (news map; economic data)"

# Indicator ID -> snapshot key; we take the latest available value and year.
INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp_current_usd",      # GDP (current US$)
    "NY.GDP.PCAP.CD": "gdp_per_capita_usd",   # GDP per capita (current US$)
    "NY.GDP.MKTP.KD.ZG": "gdp_growth_pct",    # GDP growth (annual %)
    "FP.CPI.TOTL.ZG": "inflation_cpi_pct",    # Inflation, consumer prices (annual %)
    "SL.UEM.TOTL.ZS": "unemployment_pct",     # Unemployment, total (% of labor force)
}


def _fetch_indicator(iso3: str, indicator_id: str) -> tuple[float | None, str | None]:
    """Fetch latest non-null value and year for one indicator. Returns (value, year) or (None, None)."""
    url = (
        f"{BASE_URL}/country/{iso3.lower()}/indicator/{indicator_id}"
        f"?format=json&per_page=10&date=2010:2030"
    )
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            data = resp.read().decode()
    except (urllib.error.URLError, OSError, ValueError) as e:
        log.debug("World Bank request failed for %s %s: %s", iso3, indicator_id, e)
        return None, None
    try:
        import json
        parsed = json.loads(data)
    except Exception:
        return None, None
    if not isinstance(parsed, list) or len(parsed) < 2 or not parsed[1]:
        return None, None
    for row in parsed[1]:
        val, year = row.get("value"), row.get("date")
        if val is not None and year is not None:
            try:
                return float(val), str(year)
            except (TypeError, ValueError):
                continue
    return None, None


def get_world_bank_snapshot(iso3: str) -> dict[str, Any]:
    """
    Fetch latest available macro indicators for a country (ISO 3166-1 alpha-3).
    Returns a dict with gdp_current_usd, gdp_per_capita_usd, gdp_growth_pct,
    inflation_cpi_pct, unemployment_pct, year (latest year present), source.
    Omit fields when data is missing; never raise.
    """
    result: dict[str, Any] = {
        "source": "World Bank",
    }
    latest_year: str | None = None
    for ind_id, key in INDICATORS.items():
        value, year = _fetch_indicator(iso3, ind_id)
        if value is not None:
            result[key] = value
            if year and (latest_year is None or (year > latest_year)):
                latest_year = year
    if latest_year:
        result["year"] = latest_year
    return result
