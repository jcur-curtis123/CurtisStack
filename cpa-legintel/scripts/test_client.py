from app.database import SessionLocal
from app.services.client_service import create_client

db = SessionLocal()

client = create_client(
    db,
    name="Acme Construction LLC",
    entity_type="LLC",
    state="ME",
)

print(client.id, client.name)
db.close()
