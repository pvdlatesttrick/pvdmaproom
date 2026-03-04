# News Map (Flask + Leaflet)

Beginner-friendly project that plots news stories on a live world map.

## What it does

- Flask web app serves a Leaflet map at `/`
- JSON API at `/api/stories`
- Ingestion command fetches world RSS feeds from BBC, Economist, Reuters, Wall Street Journal, Washington Post, New York Times, and Axios
- Ingestion can also include verified X reports/videos (from curated high-trust accounts) when location can be inferred
- Additional regional feeds are included for Africa and the Middle East
- Stories are stored in SQLite; the same story can appear in multiple countries when relevant
- Place names are guessed with a stricter heuristic and geocoded with cache. If location cannot be inferred, an optional **LLM** (OpenAI-compatible API) can infer relevant countries so the story is added to the map only where it is relevant
- Source logos are shown in map markers and in each story popup
- Story popups include CIA World Factbook fields for the resolved country (capital, population, GDP PPP, area, government type)
- Country borders are clickable; clicking a country highlights it and opens a side panel with CIA facts plus Economist and recent country stories
- Country side panel title shows original/local country name with English in parentheses

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

3. **Ingest runs automatically** when the app starts (in a background thread), so the map will fill with stories after a minute or two. To run ingest manually (e.g. to refresh data):  
   `docker compose run --rm web python -m app.ingest`  
   Or trigger it via **POST** `/api/ingest` (returns 202 immediately; ingest runs in background).

4. Refresh browser. Markers should appear (the page also auto-polls every 30s).

## Public access (shareable link)

To get a **public URL** that works from anywhere (not just localhost):

### Option A: Deploy to Render (free)

1. Push this repo to GitHub (if you haven’t already).
2. Go to [dashboard.render.com](https://dashboard.render.com), sign in, and click **New → Web Service**.
3. Connect your GitHub account and select the `pvdmaproom` repo.
4. Render will use the repo’s `render.yaml` (build and start commands). Click **Create Web Service**.
5. After the first deploy, your map will be at a URL like **`https://pvdmaproom.onrender.com`** (or the name you gave the service). Use that link to open the map from any device.
6. **Stories load automatically**: ingest runs in the background when the app starts, so the map will populate shortly after deploy. On Render’s free tier the disk is **ephemeral** (DB resets on restart), so each deploy/restart triggers a fresh ingest. To refresh data without restarting, call **POST** `/api/ingest` (e.g. from a cron job or manually).  
   **Optional**: set `NYT_API_KEY` in Render’s Environment (Dashboard → your service → Environment) to pull **NYT Top Stories (World)** from the NYT API in addition to the NYT World RSS feed. Without it, NYT still appears via RSS; with it you get more NYT stories on the map.

### Option B: ngrok (quick tunnel from your machine)

1. Run the app locally: `docker compose up` (or `gunicorn -b 0.0.0.0:8000 "app.main:create_app()"`).
2. Install [ngrok](https://ngrok.com/download) and run: `ngrok http 8000`.
3. Use the **HTTPS** URL ngrok shows (e.g. `https://abc123.ngrok.io`) as your public link. It works until you close ngrok.

## Included news sources

All of these are currently used via **public RSS/Atom feeds** (no API key required):

- BBC World, BBC Asia, BBC Africa, BBC Middle East
- The Economist (The World This Week, Asia, MEA, Graphic detail)
- The Guardian, Politico, The Dispatch
- Reuters, Wall Street Journal World, Washington Post World, Axios
- Al Jazeera, DW, CNN, NBC, Sky News
- Rudaw English, Middle East Eye
- Government feeds (US, UK, EU, Canada, Brazil, Japan, India, and many others)
- Amnesty, HRW, Carnegie, AEI, Hudson
- X/Twitter posts via Nitter RSS mirrors (no Twitter API key)
- ESPN and other sports feeds

**New York Times**: There is an NYT World RSS feed in the list above, so some NYT stories already appear. To add **NYT Top Stories (World)** from the official API (more stories, richer metadata), set the environment variable **`NYT_API_KEY`** (e.g. in Render: Dashboard → your service → Environment). Get a free key at [developer.nytimes.com](https://developer.nytimes.com/apis).

### Sources we don’t have APIs for (and what would be needed)

- **No other paid or key-gated APIs are required.** All other integrated outlets are reached via public RSS/Atom or Nitter. If you want to add a source that only offers an API (e.g. some paywalled sites), you’d need: (1) an API key or auth from that provider, (2) a small adapter in `app/sources/` that fetches and normalizes stories, and (3) a call to that adapter in `run_ingest()` when the key is set (same pattern as `NYT_API_KEY` + `fetch_nyt_top_stories`).

## Economist-style rankings

The country panel shows **Economist-style rankings** (e.g. Democracy Index) when available. Data is refreshed each time you run ingest. To use your own data when The Economist updates:

- **CSV**: set `ECONOMIST_RANKINGS_DEMOCRACY_URL` to a URL that returns CSV with columns `country`, `score` (and optionally `rank`, `year`).
- **JSON**: set `ECONOMIST_RANKINGS_DEMOCRACY_JSON_URL` to a URL that returns a JSON array of `{ "country", "score", "rank?", "year?" }`.

If neither is set, a small bundled snapshot (Democracy Index) is used so the feature works out of the box. See [The Economist rankings calendar](https://www.economist.com/news/2009/05/29/rankings-calendar) for publication schedules.

## Location inference (optional)

When a story’s location cannot be resolved from the text, ingest can call an LLM to infer which countries the article is relevant to, and add the story only there (one pin per relevant country). To enable this:

1. Install the dependency: `pip install openai`
2. Set `OPENAI_API_KEY` (or use another OpenAI-compatible API and set `OPENAI_BASE_URL`).
3. Optionally set `LOCATION_MODEL` (default: `gpt-4o-mini`).

If the key is not set, ingest skips the model step and only adds stories that geocode successfully.

## CIA Factbook data

By default ingestion downloads Factbook JSON from:

`https://raw.githubusercontent.com/iancoleman/cia_world_factbook_api/master/data/factbook.json`

You can override this with:

```bash
export CIA_FACTBOOK_URL="https://your-factbook-json-url"
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

