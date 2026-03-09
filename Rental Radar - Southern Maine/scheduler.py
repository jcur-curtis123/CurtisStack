import asyncio
import traceback
from datetime import datetime, timezone
from sources import SOURCES
from db import upsert_listing


def now_iso():
    return datetime.now(timezone.utc).isoformat()


async def run_single_source(conn, source):
    name = source["name"]
    fn = source["fn"]

    print(f"TASK STARTED FOR SOURCE: {name}")

    job_id = None

    try:
        started = now_iso()
        cur = conn.execute(
            "INSERT INTO scrape_jobs (started_at, status) VALUES (?, ?)",
            (started, f"running:{name}")
        )
        job_id = cur.lastrowid
        conn.commit()

        result = fn()

        # Handle sync or async functions
        if asyncio.iscoroutine(result):
            listings = await result
        else:
            listings = result

        print(f"{name} returned {len(listings)} listings")

        new_count = 0
        for listing in listings:
            if upsert_listing(conn, listing):
                new_count += 1

        conn.execute(
            "UPDATE scrape_jobs SET finished_at=?, status=?, listings_found=?, new_listings=? WHERE id=?",
            (now_iso(), "success", len(listings), new_count, job_id)
        )

        conn.commit()

    except Exception as e:
        print(f"[ERROR] Source={name}")
        traceback.print_exc()

        if job_id:
            conn.execute(
                "UPDATE scrape_jobs SET finished_at=?, status=?, error=? WHERE id=?",
                (now_iso(), "failed", str(e), job_id)
            )
            conn.commit()


async def run_scrape_loop(conn):
    print("SCRAPE LOOP STARTED")

    while True:
        tasks = []

        for source in SOURCES:
            if not source.get("enabled", True):
                continue

            tasks.append(run_single_source(conn, source))

        if tasks:
            await asyncio.gather(*tasks)

        await asyncio.sleep(60)
