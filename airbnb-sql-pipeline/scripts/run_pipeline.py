import os
import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_CSV = BASE_DIR / "data" / "raw" / "Airbnb_Open_Data.csv"
DB_PATH = BASE_DIR / "db" / "airbnb.db"

SCHEMA_SQL = BASE_DIR / "db" / "schema.sql"
SQL_STAGING = BASE_DIR / "sql" / "01_staging.sql"
SQL_MARTS = BASE_DIR / "sql" / "02_marts.sql"
SQL_QUERIES = BASE_DIR / "sql" / "03_queries.sql"

OUT_DIR = BASE_DIR / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_raw(conn: sqlite3.Connection):
    # Create raw table
    conn.executescript(SCHEMA_SQL.read_text())

    # Read CSV (keep as strings to match schema and avoid dtype friction)
    df = pd.read_csv(RAW_CSV, dtype=str, low_memory=False)

    # Rename columns to match schema (normalize casing and spaces)
    rename_map = {
        "NAME": "name",
        "host id": "host_id",
        "host_identity_verified": "host_identity_verified",
        "host name": "host_name",
        "neighbourhood group": "neighbourhood_group",
        "neighbourhood": "neighbourhood",
        "lat": "lat",
        "long": "long",
        "country code": "country_code",
        "instant_bookable": "instant_bookable",
        "cancellation_policy": "cancellation_policy",
        "room type": "room_type",
        "Construction year": "construction_year",
        "price": "price",
        "service fee": "service_fee",
        "minimum nights": "minimum_nights",
        "number of reviews": "number_of_reviews",
        "last review": "last_review",
        "reviews per month": "reviews_per_month",
        "review rate number": "review_rate_number",
        "calculated host listings count": "calculated_host_listings_count",
        "availability 365": "availability_365",
        "house_rules": "house_rules",
    }
    # normalize base columns
    df = df.rename(columns=rename_map)

    # expected is a list of raw column headers
    # this will be utilized for potential missing columns
    expected = [
        "id","name","host_id","host_identity_verified","host_name",
        "neighbourhood_group","neighbourhood","lat","long","country","country_code",
        "instant_bookable","cancellation_policy","room_type","construction_year",
        "price","service_fee","minimum_nights","number_of_reviews","last_review",
        "reviews_per_month","review_rate_number","calculated_host_listings_count",
        "availability_365","house_rules","license"
    ]

    # Try Catch for potential misisng columns
    missing = [c for c in expected if c not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing expected columns: {missing}")

    df = df[expected]

    # Load into SQLite
    df.to_sql("raw_listings", conn, if_exists="append", index=False)
    conn.commit()
    print(f"Loaded {len(df):,} rows into raw_listings")


def exec_sql(conn: sqlite3.Connection, path: Path) -> None:
    conn.executescript(path.read_text())
    conn.commit()
    print(f"Executed: {path.name}")


def export_query_results(conn: sqlite3.Connection) -> None:
    sql_text = SQL_QUERIES.read_text()
    # Split by semicolon, keep statements with SELECT
    statements = [s.strip() for s in sql_text.split(";") if s.strip()]
    selects = [s for s in statements if s.upper().startswith("SELECT")]

    out_files = [
        OUT_DIR / "avg_price_by_neighborhood_top25.csv",
        OUT_DIR / "host_leaderboard_top25.csv",
        OUT_DIR / "room_type_distribution.csv",
    ]
    for stmt, out_path in zip(selects, out_files):
        df = pd.read_sql_query(stmt, conn)
        df.to_csv(out_path, index=False)
        print(f"Wrote: {out_path.relative_to(BASE_DIR)} ({len(df)} rows)")


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()  # rebuild for reproducibility

    with sqlite3.connect(DB_PATH) as conn:
        load_raw(conn)
        exec_sql(conn, SQL_STAGING)
        exec_sql(conn, SQL_MARTS)
        export_query_results(conn)

    print("\nDone. Open db/airbnb.db with any SQLite viewer")


if __name__ == "__main__":
    main()
