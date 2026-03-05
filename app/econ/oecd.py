"""
OECD Statistics API – optional enrichment for OECD members only.
Free API: https://data.oecd.org/api/sdmx-json-documentation/
If data is not available for a country, return {}.
"""

from __future__ import annotations

import logging
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

log = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10
USER_AGENT = "pvdmaproom/1.0 (news map; economic data)"

# OECD members (ISO 3166-1 alpha-3). Used to skip API calls for non-members.
OECD_ISO3 = frozenset({
    "AUS", "AUT", "BEL", "CAN", "CHL", "COL", "CRI", "CZE", "DNK", "EST", "FIN",
    "FRA", "DEU", "GRC", "HUN", "ISL", "IRL", "ISR", "ITA", "JPN", "KOR", "LVA",
    "LTU", "LUX", "MEX", "NLD", "NZL", "NOR", "POL", "PRT", "SVK", "SVN", "ESP",
    "SWE", "CHE", "TUR", "GBR", "USA",
})


def get_oecd_enrichment(iso3: str) -> dict[str, Any]:
    """
    Fetch a couple of extra indicators for OECD members only (e.g. unemployment detail,
    trade openness). Returns {} for non-OECD or on failure. Kept minimal.
    """
    if not iso3 or (iso3.upper() if isinstance(iso3, str) else "") not in OECD_ISO3:
        return {}
    result: dict[str, Any] = {}
    try:
        _fetch_oecd_indicators(iso3.upper(), result)
    except Exception as e:
        log.debug("OECD fetch failed for %s: %s", iso3, e)
    return result


def _fetch_oecd_indicators(iso3: str, out: dict[str, Any]) -> None:
    """Try MEI or similar dataset for unemployment. SDMX-JSON structure; optional enrichment."""
    # OECD.Stat uses dataset/dimension filters. MEI LUR = unemployment; country code ISO3.
    url = f"https://stats.oecd.org/SDMX-JSON/data/MEI/LUR.{iso3}/all?contentType=json"
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
    data_sets = data.get("dataSets") or []
    if not data_sets:
        return
    series_list = data_sets[0].get("series")
    if not isinstance(series_list, dict):
        return
    for _sid, s in series_list.items():
        obs = s.get("observations") or {}
        if not obs:
            continue
        keys = sorted((k for k in obs if isinstance(k, str) and k.isdigit()), key=int, reverse=True)
        if keys:
            v = obs[keys[0]]
            if isinstance(v, list) and len(v) > 0:
                try:
                    out["unemployment_detail_pct"] = float(v[0])
                    break
                except (TypeError, ValueError):
                    pass
    if out:
        out.setdefault("source", "OECD")
