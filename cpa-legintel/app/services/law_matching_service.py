from sqlalchemy.orm import Session
from app.models import Client, Law, LawVersion, LawImpact


def generate_law_impact(
    db: Session,
    client: Client,
    law: Law,
    version: LawVersion,
) -> LawImpact:
    """
    Stubbed AI impact generator.
    Replace with real LLM call in Step 9.
    """

    summary = (
        f"This regulation may affect {client.name} "
        f"because it applies to entities operating in {client.state}."
    )

    impact = LawImpact(
        client_id=client.id,
        law_id=law.id,
        law_version_id=version.id,
        summary=summary,
        reasoning="Stubbed impact logic",
        confidence=0.4,
    )

    db.add(impact)
    db.commit()
    db.refresh(impact)
    return impact
