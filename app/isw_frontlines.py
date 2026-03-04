"""ISW-style front-line GeoJSON for the Conflicts map.
Update coordinates from ISW maps or other open sources as needed.
Format: GeoJSON FeatureCollection of LineString features.
Coordinates: [longitude, latitude] (GeoJSON standard)."""

# Approximate/indicative front lines; replace with updated data as available.
# Source: ISW and similar public maps. Update periodically.
ISW_FRONTLINES_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": "Ukraine (approx. front line)", "updated": "2024"},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [32.4, 51.5],
                    [33.2, 51.0],
                    [34.0, 50.5],
                    [35.2, 50.0],
                    [36.5, 49.5],
                    [37.8, 49.0],
                    [38.5, 48.6],
                    [39.0, 48.2],
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {"name": "Ukraine (south)", "updated": "2024"},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [34.2, 47.8],
                    [35.0, 47.5],
                    [36.0, 47.2],
                    [37.0, 47.0],
                ],
            },
        },
    ],
}
