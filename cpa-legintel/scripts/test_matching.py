from app.database import SessionLocal
from app.models import Client
from app.services.law_matching import match_laws_to_client

db = SessionLocal()

client = db.query(Client).first()
count = match_laws_to_client(db, client)

print(f"Matched {count} laws to {client.name}")
db.close()
