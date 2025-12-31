# Airbnb SQL-First Data Pipeline (SQLite + Python)

This repo is a SQL-architecture data pipeline built around the provided dataset `Airbnb_Open_Data.csv`.

The pipeline is intentionally split into layers:

- Load the source CSV into a `raw_listings` table.
- Clean/standardize column names, types, and formats in `stg_listings`.
- Create tables:
  - `dim_host`
  - `dim_neighborhood`
  - `fct_listings`
- Example analytics outputs written to `data/processed/`.

## To start

```bash
cd airbnb-sql-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/run_pipeline.py
```

## Outputs:
- SQLite DB at `db/airbnb.db`
- CSVs in `data/processed/` (materialized query results)

All transformations from raw → staging → marts happen in versioned SQL files in `sql/`.

Python is used to load and execute the results from the SQL query.