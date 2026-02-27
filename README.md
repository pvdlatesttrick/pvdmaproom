# News Map (Flask + Leaflet)

Beginner-friendly project that plots news stories on a world map.

## What it does

- Flask web app serves a Leaflet map at `/`
- JSON API at `/api/stories`
- Ingestion command fetches BBC RSS (and optionally NYT)
- Stories are stored in SQLite with URL deduplication
- Place names are guessed with a simple heuristic, then geocoded with cache

## Project layout

- `app/main.py` - Flask app + routes
- `app/ingest.py` - ingestion command (`python -m app.ingest`)
- `app/db.py` - SQLite setup and queries
- `app/sources/` - source-specific fetchers
- `app/templates/index.html` - Leaflet frontend

## Run with Docker (recommended)

1. Build and start web app:

```bash
docker compose up --build
```

2. Open:

`http://localhost:8000`

3. In another terminal, ingest stories:

```bash
docker compose run --rm web python -m app.ingest
```

4. Refresh browser. Markers should appear (the page also auto-polls every 30s).

## Optional NYT API

Set env var before ingest:

```bash
export NYT_API_KEY="your_api_key"
docker compose run --rm web python -m app.ingest
```

## Local run (without Docker)

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Use a local DB path (instead of `/data/app.db`):

```bash
export DB_PATH="./data/app.db"
python -m app.ingest
gunicorn -b 0.0.0.0:8000 "app.main:create_app()"
```

