import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

def _uuid() -> str:
    return str(uuid.uuid4())

class Base(DeclarativeBase):
    pass

class Law(Base):
    __tablename__ = "laws"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uuid)
    law_code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    title: Mapped[str] = mapped_column(Text)
    authority: Mapped[str] = mapped_column(String(64))
    citation: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    versions = relationship("LawVersion", back_populates="law")

class LawVersion(Base):
    __tablename__ = "law_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    law_id: Mapped[str] = mapped_column(String, ForeignKey("laws.id"), index=True)
    text: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    source_url: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    law = relationship("Law", back_populates="versions")
class Client(Base):
    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=_uuid
    )

    name: Mapped[str] = mapped_column(Text, index=True)
    entity_type: Mapped[str] = mapped_column(String(64))
    state: Mapped[str] = mapped_column(String(2))

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )


class ClientLaw(Base):
    __tablename__ = "client_laws"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=_uuid
    )

    client_id: Mapped[str] = mapped_column(
        String, ForeignKey("clients.id"), index=True
    )

    law_id: Mapped[str] = mapped_column(
        String, ForeignKey("laws.id"), index=True
    )

    applies: Mapped[bool] = mapped_column(default=True)
    confidence: Mapped[float] = mapped_column(default=1.0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
class LawImpact(Base):
    __tablename__ = "law_impacts"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=_uuid
    )

    client_id: Mapped[str] = mapped_column(
        String, ForeignKey("clients.id"), index=True
    )

    law_id: Mapped[str] = mapped_column(
        String, ForeignKey("laws.id"), index=True
    )

    law_version_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("law_versions.id"), index=True
    )

    summary: Mapped[str] = mapped_column(Text)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)

    confidence: Mapped[float] = mapped_column(default=0.5)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
