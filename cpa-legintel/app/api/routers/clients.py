# app/api/routers/clients.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.client import Client

router = APIRouter()

@router.get("/")
def list_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Client).filter(Client.user_id == current_user.id).all()

@router.post("/")
def create_client(
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client = Client(name=name, user_id=current_user.id)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.get("/{client_id}")
def get_client(
    client_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    client = (
        db.query(Client)
        .filter(Client.id == client_id, Client.user_id == current_user.id)
        .one_or_none()
    )
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client
