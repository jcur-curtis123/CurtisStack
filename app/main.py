# app/main.py

from fastapi import FastAPI
from app.api.routers import auth, clients

app = FastAPI(title="CPA LegIntel", version="0.1.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(clients.router, prefix="/clients", tags=["clients"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
