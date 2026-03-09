from app.database import SessionLocal
from app.models import Client, Law, LawVersion
from app.services.law_impact_service import generate_law_impact

db = SessionLocal()

client = db.query(Client).first()
law = db.query(Law).first()
version = (
    db.query(LawVersion)
    .filter(LawVersion.law_id == law.id)
    .order_by(LawVersion.created_at.desc())
    .first()
)

impact = generate_law_impact(db, client, law, version)
print("SUMMARY:", impact.summary)
print("CONFIDENCE:", impact.confidence)

db.close()
