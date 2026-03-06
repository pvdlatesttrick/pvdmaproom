# Country news seed data

This folder backs the **country news** pipeline so every country can show at least one item in the sidebar and a pin when the country is selected. The backend uses `get_country_news(country_name)` (in `app/country_news.py`), which reads seed data here; if a country has no seed entry, it still returns one generic overview item so the UI is never empty.

## Data pipeline

1. **API:** `GET /api/country?name=...` → `get_country_detail()` in `app/db.py`.
2. **Stories** come from: (1) DB stories from the ingest pipeline (RSS/news APIs), (2) seed items from `get_country_news()` (this folder), (3) if still empty, one placeholder from `get_placeholder_story()`.
3. **Map:** When a user clicks a country, the frontend calls `/api/country`, then draws markers from `recent_stories` (each item has `lat`/`lon` from seed or centroid) and fills the sidebar from `all_source_stories` / `recent_stories`.

## Files

- **seed.json** – Per-country news items keyed by ISO 3166-1 alpha-2 (e.g. `US`, `FR`). Structure:
  - `countries`: object whose keys are ISO2 codes and values are arrays of items.
  - Each item: `title`, `summary`, `source_url`, `date`, `source`, optional `lat`/`lon`, optional `topic` (`geopolitics` | `economics` | `conflicts` | `sports`).
- **centroids.json** – Fallback coordinates when a seed item has no `lat`/`lon`. Keys are ISO2, values are `[lat, lon]`.

## Editing by hand

1. Open `seed.json`.
2. Add or edit entries under `countries.<ISO2>`, e.g. `countries.MM` for Myanmar.
3. Save. Use **Admin → Seed** and click “Clear seed cache” so the next country click loads the new data (or restart the app).

## Seeding all countries (placeholders)

From the project root:

```bash
python3 scripts/seed_country_news.py
```

This adds one generic placeholder per country that has no entry yet (with `lat`/`lon` from `centroids.json` when available); existing entries are left unchanged. Install `pycountry` for full country names: `pip install pycountry`.

## Admin

- **Admin → Seed** (or `/admin/seed`) explains the format, offers a download of the current `seed.json`, and a “Clear seed cache” button after you replace the file.
- **Download current seed.json** – edit locally and replace in `app/data/country_news/`, then clear the cache or restart.
