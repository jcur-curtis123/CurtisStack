from sqlalchemy.orm import Session
from app.models import Law, LawVersion
from app.collectors.canonical import canonical_law_text
from app.collectors.hashing import sha256
from app.services.law_impact_service import generate_law_impact
from app.models import ClientLaw

def upsert_law_version(db: Session, doc: dict) -> bool:
    law_code = doc.get("document_number")
    if not law_code:
        return False

    law = db.query(Law).filter(Law.law_code == law_code).one_or_none()
    if not law:
        law = Law(
            law_code=law_code,
            title=doc.get("title"),
            authority="Federal Register",
            citation=doc.get("html_url"),
        )
        db.add(law)
        db.flush()

    text = canonical_law_text(doc)
    new_hash = sha256(text)

    latest = (
        db.query(LawVersion)
        .filter(LawVersion.law_id == law.id)
        .order_by(LawVersion.created_at.desc())
        .first()
    )

    if latest and latest.content_hash == new_hash:
        return False

    db.add(
        LawVersion(
            law_id=law.id,
            text=text,
            content_hash=new_hash,
            source_url=doc.get("html_url"),
        )
    )
    return True
