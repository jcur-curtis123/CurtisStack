# app/models/law.py

import uuid
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base


class Law(Base):
    __tablename__ = "laws"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # core identifiers
    title = Column(String, nullable=False)
    agency = Column(String, nullable=True)
    jurisdiction = Column(String, nullable=True)

    # optional metadata
    summary = Column(Text, nullable=True)
    source_url = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
