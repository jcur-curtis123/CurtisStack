from pathlib import Path
import sqlite3
import pandas as pd

# -----------------------------
# Paths (NO ambiguity)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_CSV = BASE_DIR / "data" / "raw" / "Airbnb_Open_Data.csv"
DB_PATH = BASE_DIR / "db" / "airbnb.db"
OUT_DIR = BASE_DIR / "data" / "processed"

SCHEMA_SQL = BASE_DIR / "db" / "schema.sql"
STAGING_SQL = BASE_DIR / "sql" / "01_staging.sql"
MARTS_SQL = BASE_DIR / "sql" / "02_marts.sql"

OUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load raw data
# -----------------------------
def load_raw(conn):
    print(f"Loading raw CSV from:\n{RAW_CSV}")

    conn.executescript(SCHEMA_SQL.read_text())

    df = pd.read_csv(RAW_CSV, dtype=str, low_memory=False)

    # normalize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    df.to_sql("raw_listings", conn, if_exists="append", index=False)
    conn.commit()

    print(f"Loaded {len(df):,} rows into raw_listings")

# -----------------------------
# Run SQL file
# -----------------------------
def run_sql(conn, path):
    print(f"Executing: {path.name}")
    conn.executescript(path.read_text())
    conn.commit()

# -----------------------------
# Export analytics (EXPLICIT)
# -----------------------------
def export_results(conn):
    print(f"Exporting analytics to:\n{OUT_DIR}")

    queries = {
        "avg_price_by_neighborhood.csv": """
            SELECT neighborhood_group, neighborhood,
                   COUNT(*) AS listings,
                   ROUND(AVG(price_usd), 2) AS avg_price
            FROM fct_listings
            WHERE price_usd IS NOT NULL
            GROUP BY neighborhood_group, neighborhood
            ORDER BY avg_price DESC
            LIMIT 25;
        """,

        "host_leaderboard.csv": """
            SELECT host_id,
                   COUNT(*) AS listings,
                   ROUND(AVG(price_usd), 2) AS avg_price
            FROM fct_listings
            GROUP BY host_id
            ORDER BY listings DESC
            LIMIT 25;
        """,

        "room_type_distribution.csv": """
            SELECT room_type,
                   COUNT(*) AS listings,
                   ROUND(AVG(price_usd), 2) AS avg_price
            FROM fct_listings
            WHERE room_type IS NOT NULL
            GROUP BY room_type;
        """
    }

    for filename, sql in queries.items():
        out_path = OUT_DIR / filename
        df = pd.read_sql_query(sql, conn)
        df.to_csv(out_path, index=False)

        print(f"WROTE → {out_path} ({len(df)} rows)")

# -----------------------------
# Main
# -----------------------------
def main():
    print("\n--- STARTING AIRBNB PIPELINE ---\n")

    if DB_PATH.exists():
        DB_PATH.unlink()

    with sqlite3.connect(DB_PATH) as conn:
        load_raw(conn)
        run_sql(conn, STAGING_SQL)
        run_sql(conn, MARTS_SQL)
        export_results(conn)

    print("\nPIPELINE COMPLETE ✅")
    print(f"CHECK THIS FOLDER:\n{OUT_DIR}\n")

if __name__ == "__main__":
    main()
