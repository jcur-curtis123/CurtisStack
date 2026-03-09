import datetime as dt
from app.database import SessionLocal
from app.collectors.federal_register import fetch_documents
from app.services.law_versioning import upsert_law_version

def run():
    db = SessionLocal()
    try:
        start = dt.date.today() - dt.timedelta(days=2)
        end = dt.date.today()

        created = 0
        for doc in fetch_documents(start, end):
            if upsert_law_version(db, doc):
                created += 1

        db.commit()
        print(f"✅ Ingest complete — {created} new law versions")
    finally:
        db.close()

if __name__ == "__main__":
    run()
