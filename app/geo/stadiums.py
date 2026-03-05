"""Stadium/venue lookup for precise sports story geocoding (campus, arena, ground)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_STADIUMS: list[dict[str, Any]] | None = None
_STADIUMS_BY_TEAM: dict[str, dict[str, Any]] = {}


def _load_stadiums() -> None:
    global _STADIUMS, _STADIUMS_BY_TEAM
    if _STADIUMS is not None:
        return
    path = Path(__file__).resolve().parent.parent / "data" / "stadiums.json"
    if not path.exists():
        _STADIUMS = []
        return
    with path.open("r", encoding="utf-8") as f:
        _STADIUMS = json.load(f)
    for s in _STADIUMS:
        key = (s.get("team_key") or "").strip().lower()
        if key:
            _STADIUMS_BY_TEAM[key] = s


def get_stadium_for_team(team_key: str) -> dict[str, Any] | None:
    """
    Return stadium record (lat, lon, city, country, stadium_name) for a normalized team_key,
    or None if not found.
    """
    if not (team_key and isinstance(team_key, str)):
        return None
    _load_stadiums()
    key = team_key.strip().lower()
    return _STADIUMS_BY_TEAM.get(key)
