from sqlalchemy.orm import Session
from app.models import Client, Law, ClientLaw


def match_laws_to_client(
    db: Session,
    client: Client,
) -> int:
    """
    Naive first pass:
    attach ALL laws to client with low confidence.
    Later this becomes AI-driven.
    """

    laws = db.query(Law).all()
    created = 0

    for law in laws:
        exists = (
            db.query(ClientLaw)
            .filter(
                ClientLaw.client_id == client.id,
                ClientLaw.law_id == law.id,
            )
            .one_or_none()
        )

        if exists:
            continue

        db.add(
            ClientLaw(
                client_id=client.id,
                law_id=law.id,
                applies=True,
                confidence=0.2,  # placeholder
            )
        )
        created += 1

    db.commit()
    return created
