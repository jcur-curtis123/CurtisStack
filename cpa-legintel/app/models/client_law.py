# app/models/client_law.py

import uuid
from sqlalchemy import (
    Column,
    Boolean,
    Float,
    Text,
    DateTime,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.base import Base



class ClientLaw(Base):
    __tablename__ = "client_laws"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # 🔐 tenancy boundary inherited via client
    client_id = Column(
        UUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # regulation reference
    law_id = Column(
        UUID(as_uuid=True),
        ForeignKey("laws.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # AI output fields
    applies = Column(Boolean, nullable=False, default=False)
    confidence = Column(Float, nullable=False, default=0.0)
    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
