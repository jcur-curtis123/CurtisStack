# FieldMatch

Address in, zoning answer out. A small tool for the "can I build a duplex
here?" question: geocode an address, find the containing parcel, and check
its zoning against Maine's LD 2003 statewide housing-density law.

```
frontend/   React + Vite UI — address/question form, structured result view
backend/    FastAPI service — geocoding, parcel lookup, zoning logic
```

## Quickstart

Terminal 1:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Terminal 2:
```bash
cd frontend
npm install
npm run dev
```

Open the Vite dev URL (usually http://localhost:5173), enter an address in
downtown Portland, ME (the bundled demo data only covers that area — see
`backend/README.md` to swap in real parcel data), and hit "Analyze parcel."

## What's actually implemented

- **Geocoding** (`backend/app/geocode.py`) — real address -> lat/lon via
  OpenStreetMap Nominatim, with an offline-safe fallback.
- **Parcel lookup** (`backend/app/spatial.py`) — spatial-indexed
  point-in-polygon search, not a linear scan; works against either the
  bundled demo GeoJSON or a real `parcels.shp`/`.geojson` dropped into
  `backend/data/`, with case-insensitive field-name matching for real
  assessor exports.
- **Zoning eligibility** (`backend/app/zoning.py`) — a real rules model
  based on Maine's LD 2003 (2-unit floor statewide, 4-unit in growth areas,
  carve-outs for shoreland/non-residential zones, a practical caveat on
  very small lots), not a hardcoded string.
- **API** (`backend/app/main.py`) — CORS enabled so the frontend can
  actually call it; returns parcel details, the eligibility reasoning,
  caveats, and a confidence score.
- **Frontend** (`frontend/src/App.jsx`) — a real form (not a single hardcoded
  button), loading/error states, and a structured parcel-record view instead
  of a raw JSON dump. Vite's dev server proxies `/api/*` to `localhost:8000`
  (see `frontend/vite.config.js`), so the frontend never hardcodes a host.

## Known limitations / next steps

- Demo parcel data is synthetic — real deployment needs an actual municipal
  `parcels.shp` (many Maine towns publish these via their GIS office or
  Maine's statewide GIS portal).
- Zoning logic is a simplified general model of LD 2003, not a parsed
  version of any specific municipality's ordinance — treat answers as a
  starting point, not a permit decision.
- No caching on the geocoder — fine for a demo, worth adding if this sees
  real traffic (Nominatim's usage policy caps at ~1 req/sec).
- No automated test suite yet — worth adding `pytest` coverage for
  `zoning.py`'s rules and `spatial.py`'s column-normalization once real
  parcel data is in the mix.
