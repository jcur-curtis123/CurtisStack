from sqlalchemy.orm import Session
from app.models import Client


def create_client(
    db: Session,
    name: str,
    entity_type: str,
    state: str,
) -> Client:
    client = Client(
        name=name,
        entity_type=entity_type,
        state=state,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client
