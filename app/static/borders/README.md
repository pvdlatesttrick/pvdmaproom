# Historical country borders (year-specific)

Border GeoJSON files in this folder drive the map’s **border year** selector. Each file should be a GeoJSON `FeatureCollection` of country polygons with at least:

- `properties.name` – country name for that year (e.g. "Yugoslavia", "West Germany")
- `properties.iso_code` or `properties.ccode` – stable identifier for mapping to stories

## Data source: CShapes

- **CShapes** (historical country boundaries): https://icr.ethz.ch/data/cshapes/
- Preprocess CShapes shapefiles into one GeoJSON per year, e.g.:
  - `borders_1960.geojson`
  - `borders_1989.geojson`
  - `borders_2000.geojson`
  - `borders_2025.geojson`

Place the generated files here. The app loads `/static/borders/borders_<year>.geojson` when the user changes the “Borders year” selector. If a file is missing, the map falls back to the default modern borders (e.g. johan/world.geo.json).

## Placeholder files

The repo may include minimal placeholder `borders_*.geojson` files so the UI works before real CShapes data is added. Replace them with full CShapes-derived GeoJSON for correct historical borders (e.g. 1960 Balkans, pre-1991 USSR, etc.).
