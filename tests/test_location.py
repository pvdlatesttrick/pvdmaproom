"""
Regression test: Saints/Jordan case — sports story about Cameron Jordan (person)
must pin at Caesars Superdome (New Orleans), not at Jordan the country.
"""

import pytest


def test_saints_jordan_pins_at_superdome_not_jordan_country():
    from app.geo.location import attach_location, stadium_location_from_story

    story = {
        "title": "Sources: Saints sack leader Cameron Jordan to be free agent.",
        "summary": "New Orleans Saints defensive end Cameron Jordan hit free agency.",
        "source": "espn_nfl",
        "topic": "sports",
        "team_home": "new-orleans-saints",
        "url": "https://example.com/saints-jordan",
    }
    attach_location(story)

    assert "lat" in story and "lon" in story
    assert story["country"] == "United States"
    lat, lon = story["lat"], story["lon"]
    # Caesars Superdome is in New Orleans (~29.95, -90.08)
    assert 29.5 <= lat <= 30.5
    assert -91 <= lon <= -89
    assert "New Orleans" in (story.get("place_name") or "") or "New Orleans" in (story.get("city") or "") or "Superdome" in (story.get("place_name") or "")
    assert story.get("place_name") != "Jordan"
    assert story.get("country") != "Jordan"


def test_stadium_location_from_story_uses_team_home():
    from app.geo.location import stadium_location_from_story

    story = {
        "title": "Saints sack leader Cameron Jordan to be free agent.",
        "summary": "",
        "team_home": "new-orleans-saints",
    }
    loc = stadium_location_from_story(story)
    assert loc is not None
    assert loc.get("stadium_name") == "Caesars Superdome"
    assert loc.get("city") == "New Orleans"
    assert 29.5 <= float(loc["lat"]) <= 30.5
    assert -91 <= float(loc["lon"]) <= -89


def test_stadium_location_infers_saints_from_text_when_no_team_key():
    from app.geo.location import stadium_location_from_story

    story = {
        "title": "Saints sack leader Cameron Jordan to be free agent.",
        "summary": "New Orleans Saints and Cameron Jordan.",
        "topic": "sports",
    }
    loc = stadium_location_from_story(story)
    assert loc is not None
    assert "New Orleans" in (loc.get("city") or "")
