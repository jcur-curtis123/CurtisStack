# FieldMatch backend

FastAPI service: takes an address + a plain-language question, geocodes the
address, looks up the containing parcel, and returns a zoning/duplex
eligibility answer grounded in Maine's LD 2003 density law.

## Run it

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Then visit http://localhost:8000/api/health — it'll report whether it's
running on the bundled demo data or a real shapefile.

## Demo data vs. real data

Out of the box there's no `backend/data/parcels.shp`, so the app falls back
to a small synthetic parcel grid (`app/data/sample_parcels.geojson`)
covering downtown Portland, ME with made-up but realistic zone codes. This
lets the whole pipeline — geocode -> parcel lookup -> zoning logic -> answer
— run without any external data dependency.

To use real parcel data: drop `parcels.shp` (+ its `.shx`/`.dbf`/`.prj`
sidecars) — or a `.geojson`/`.json` file — into `backend/data/`. The loader
in `app/spatial.py` picks up the first matching file automatically,
reprojects it to WGS84 if needed, and normalizes a handful of common
field-name variants case-insensitively (`MAPLOT`/`MAP_LOT`/`PID`,
`ZONE`/`ZONING`, `LOTAREA`/`LOT_AREA`, `GROWTH_AREA`, `SHORELAND`). If your
source data uses different column names for those last two flags, add the
alias to `FIELD_ALIASES` in `app/spatial.py`.

## Geocoding

Uses OpenStreetMap's Nominatim (no API key). It falls back to a fixed
downtown-Portland coordinate if the network call fails or an address
doesn't match, so the demo still works offline — that fallback is flagged
in the response (`geocoded.matched: false`) and pulls confidence down.

## Zoning logic

`app/zoning.py` implements a simplified, general-purpose model of Maine's
LD 2003: any zone that permits single-family residential use must allow at
least 2 units by right, or up to 4 in a designated growth area. Shoreland
overlays and non-residential zones are flagged as needing case-by-case
review rather than an automatic yes/no. This is a reference tool, not legal
advice or a replacement for the municipality's actual ordinance — the
response always includes caveats reminding the user to confirm locally.
