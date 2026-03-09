from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

# -------- Clients --------

class ClientCreate(BaseModel):
    name: str
    entity_type: str = Field(..., examples=["LLC", "S-Corp", "Individual"])
    state: str = Field(..., min_length=2, max_length=2, examples=["ME"])

class ClientOut(BaseModel):
    id: str
    name: str
    entity_type: str
    state: str
    created_at: datetime

    class Config:
        from_attributes = True

# -------- Laws --------

class LawOut(BaseModel):
    id: str
    law_code: str
    title: str
    authority: str
    citation: str
    created_at: datetime

    class Config:
        from_attributes = True

class LawVersionOut(BaseModel):
    id: int
    law_id: str
    content_hash: str
    source_url: str
    created_at: datetime

    class Config:
        from_attributes = True

# -------- Impacts --------

class LawImpactOut(BaseModel):
    id: str
    client_id: str
    law_id: str
    law_version_id: int
    summary: str
    reasoning: Optional[str] = None
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True
