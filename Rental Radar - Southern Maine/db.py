import sqlite3
from datetime import datetime, timezone

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def db_connect(path="rentals.db"):
    conn = sqlite3.connect(path, check_same_thread=False)
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    return conn

def upsert_listing(conn, listing):
    row = conn.execute(
        "SELECT price FROM listings WHERE source=? AND listing_id=?",
        (listing.source, listing.listing_id)
    ).fetchone()

    if row is None:
        conn.execute(
            "INSERT INTO listings VALUES (?, ?, ?, ?, ?, ?)",
            (
                listing.source,
                listing.listing_id,
                listing.title,
                listing.url,
                listing.price,
                listing.fetched_at,
            ),
        )
        conn.commit()
        return True

    old_price = row[0]

    if old_price != listing.price:
        conn.execute(
            "UPDATE listings SET price=?, fetched_at=? WHERE source=? AND listing_id=?",
            (
                listing.price,
                listing.fetched_at,
                listing.source,
                listing.listing_id,
            ),
        )
        conn.execute(
            "INSERT INTO price_history VALUES (?, ?, ?, ?, ?)",
            (
                listing.source,
                listing.listing_id,
                old_price,
                listing.price,
                now_iso(),
            ),
        )
        conn.commit()

    return False
