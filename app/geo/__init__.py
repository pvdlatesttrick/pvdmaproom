"""Geo helpers: unified location pipeline and stadium lookup."""

from app.geo.location import attach_location
from app.geo.stadiums import get_stadium_for_team

__all__ = ["attach_location", "get_stadium_for_team"]
