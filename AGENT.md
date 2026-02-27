# Cursor Agent: News Map (Flask + Leaflet) - Docker First

You are building a beginner-friendly project: a Flask app with a world map that shows news story pins.
Pins are clickable and open a popup with title, short summary, and a link to the original story.

## Goals (MVP)
1) A Flask app with:
   - GET /            -> renders an HTML page with a Leaflet world map
   - GET /api/stories -> returns JSON array of stories with lat/lon/title/summary/url/source/published_at

2) An ingestion command:
   - python -m app.ingest
   - Fetch BBC RSS feeds (World is enough for MVP)
   - Optionally fetch NYT Top Stories API if NYT_API_KEY is set

3) Store stories in SQLite:
   - db file at /data/app.db (mounted volume)
   - Deduplicate by URL (unique constraint)

4) Geo-tagging:
   - For MVP, try to derive a location from the title/summary using a simple heuristic:
     - Look for text in parentheses e.g. "(Paris)" or "(Gaza)" OR common patterns "in X", "at X"
     - If none found, set a fallback coordinate based on source region (e.g., BBC World -> London is fine)
   - Use OpenStreetMap Nominatim via geopy for geocoding with caching:
     - cache table geocode_cache(place -> lat/lon)
     - never re-geocode the same place string twice

5) Frontend:
   - Use Leaflet from CDN
   - Call /api/stories every 30 seconds and update markers
   - Each marker popup shows:
     - title (link)
     - source + published time
     - short summary (truncate to ~240 chars)

6) Docker:
   - docker compose up --build
   - app on http://localhost:8000

## Non-goals (for MVP)
- No scraping full articles
- No NLP heavy dependencies
- No auth
- No fancy UI (just clean + readable)

## Folder Layout
Create:
- app/
  - __init__.py
  - main.py
  - db.py
  - ingest.py
  - sources/
    - __init__.py
    - bbc.py
    - nyt.py
  - templates/
    - index.html
- requirements.txt
- Dockerfile
- docker-compose.yml

## Data Model
SQLite table stories:
- id INTEGER PK
- source TEXT
- title TEXT
- url TEXT UNIQUE
- summary TEXT
- published_at TEXT (ISO)
- place TEXT NULL
- lat REAL
- lon REAL
- created_at TEXT

SQLite table geocode_cache:
- place TEXT PK
- lat REAL
- lon REAL
- updated_at TEXT

## BBC Feed (MVP)
Use BBC World RSS:
- https://feeds.bbci.co.uk/news/world/rss.xml

Use feedparser to parse entries:
- title, link, summary, published

## NYT (optional)
If NYT_API_KEY exists:
Use NYT Top Stories:
- https://api.nytimes.com/svc/topstories/v2/world.json?api-key=KEY

Fields:
- title, url, abstract, published_date

## API Response
GET /api/stories returns:
[
  {
    "source": "bbc",
    "title": "...",
    "url": "...",
    "summary": "...",
    "published_at": "2026-02-27T12:34:56Z",
    "place": "Paris",
    "lat": 48.8566,
    "lon": 2.3522
  }
]

## Implementation Notes
- Use Flask app factory pattern.
- Use sqlite3 from stdlib.
- Keep code readable and heavily commented for a beginner.
- Make sure the container runs as a web server (gunicorn) and ingest can be run manually.

## Commands
- Run web: gunicorn -b 0.0.0.0:8000 "app.main:create_app()"
- Ingest: python -m app.ingest

## Deliverables
Create ALL files above with working code.
Ensure docker compose starts successfully, map loads, and markers appear after running ingest.
Also add a README.md with beginner instructions.
