from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.api.schemas import LawOut, LawVersionOut
from app.models import Law, LawVersion

router = APIRouter(prefix="/laws", tags=["laws"])


@router.get("", response_model=list[LawOut])
def list_laws(db: Session = Depends(get_db), limit: int = 50):
    return (
        db.query(Law)
        .order_by(Law.created_at.desc())
        .limit(min(limit, 200))
        .all()
    )


@router.get("/{law_id}", response_model=LawOut)
def get_law(law_id: str, db: Session = Depends(get_db)):
    law = db.get(Law, law_id)
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")
    return law


@router.get("/{law_id}/versions", response_model=list[LawVersionOut])
def list_law_versions(law_id: str, db: Session = Depends(get_db), limit: int = 20):
    law = db.get(Law, law_id)
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")

    return (
        db.query(LawVersion)
        .filter(LawVersion.law_id == law_id)
        .order_by(LawVersion.created_at.desc())
        .limit(min(limit, 100))
        .all()
    )
