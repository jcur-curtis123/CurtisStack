from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.api.schemas import LawImpactOut
from app.models import Client, LawImpact

router = APIRouter(prefix="/impacts", tags=["impacts"])


@router.get("/by-client/{client_id}", response_model=list[LawImpactOut])
def impacts_for_client(client_id: str, db: Session = Depends(get_db), limit: int = 50):
    client = db.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return (
        db.query(LawImpact)
        .filter(LawImpact.client_id == client_id)
        .order_by(LawImpact.created_at.desc())
        .limit(min(limit, 200))
        .all()
    )


@router.get("/{impact_id}", response_model=LawImpactOut)
def get_impact(impact_id: str, db: Session = Depends(get_db)):
    impact = db.get(LawImpact, impact_id)
    if not impact:
        raise HTTPException(status_code=404, detail="Impact not found")
    return impact
