"""
Economic data from free, open institutional sources (World Bank, IMF WEO, OECD).
Replaces any dependence on paywalled/licensed APIs (e.g. The Economist) for country-level macro data.
"""

from app.econ.snapshot import get_country_econ_snapshot

__all__ = ["get_country_econ_snapshot"]
