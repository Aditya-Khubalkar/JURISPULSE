"""
JurisPulse — Evidence Models
================================
Evidence items attached to a case.
Evidence can reference an uploaded document or be a standalone entry.
"""

import uuid
from typing import Optional

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDMixin


class Evidence(UUIDMixin, TimestampMixin, Base):
    """
    A piece of evidence in a case.
    May or may not be backed by an uploaded Document.
    """

    __tablename__ = "evidence"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    document_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence_type: Mapped[str] = mapped_column(String(100), nullable=False, default="DOCUMENTARY")
    source: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_ai_extracted: Mapped[bool] = mapped_column(default=False, nullable=False)
    item_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    added_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
