# Physical features layer

The **Physical features** overlay on the News Map shows major physical geography from the dataset in `physical_features.geojson`: seas, gulfs, rivers, lakes, mountain ranges, and straits. Only the **names from the data** are shown as labels (no custom points); geometries are styled by `feature_type`.

## Data format

Each feature must have:

- **geometry**: GeoJSON `Polygon`, `MultiPolygon`, `LineString`, or `MultiLineString`.
- **properties.name**: Display name (used for the label and tooltip).
- **properties.feature_type**: One of `sea`, `gulf`, `bay`, `ocean`, `lake`, `river`, `strait`, `mountain`, `plateau`. Used for styling (water = blue, mountains = brown dashed, etc.).

## Replacing with Natural Earth (1:10m)

To use full Natural Earth physical data:

1. Download from [Natural Earth 1:10m Physical Vectors](https://www.naturalearthdata.com/downloads/10m-physical-vectors/):
   - **Marine areas** (seas, gulfs): `ne_10m_geography_marine_polys`
   - **Rivers + lake centerlines**: `ne_10m_rivers_lake_centerlines` (with scale rank to filter major rivers)
   - **Lakes**: `ne_10m_lakes`
   - **Physical label areas/points**: `ne_10m_geography_regions_polys` / `ne_10m_geography_regions_points` (mountains, plateaus)

2. Convert shapefiles to GeoJSON (e.g. with [mapshaper](https://mapshaper.org/) or `ogr2ogr`), then merge or keep as separate files.

3. In `map.js`, update `loadPhysicalFeatures()` to fetch your file(s) and map Natural Earth property names (e.g. `name`, `NAME`, `featurecla`) to `name` and `feature_type` so styling and labels still work.

The current `physical_features.geojson` is a small example subset (Mediterranean, Persian Gulf, Nile, Tigris, Euphrates, Alps, Zagros, Rockies, Lake Victoria, etc.) so you can add or remove features by editing that file.
