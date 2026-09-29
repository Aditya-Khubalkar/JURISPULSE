"""
JurisPulse — Draft & DraftVersion Models
==========================================
Every AI-generated draft maintains full provenance:
  - which model generated it
  - which model version
  - generation ID from the AI service
  - latency
  - case context and sources used

Modifications create new DraftVersions — never overwrite.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.core.config.constants import DocumentType, DraftGenerationType, DraftStatus
from app.database.base import Base, TimestampMixin, UUIDMixin


class Draft(UUIDMixin, TimestampMixin, Base):
    """A legal draft associated with a case."""

    __tablename__ = "drafts"

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
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    document_type: Mapped[str] = mapped_column(
        String(100), nullable=False, default=DocumentType.OTHER.value
    )
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=DraftStatus.DRAFT.value, index=True
    )
    generation_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=DraftGenerationType.AI_GENERATED.value
    )
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    current_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Original generation instructions
    instructions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # AI model metadata — required for provenance
    # Must be NULL if no AI model was actually called
    model_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    model_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    generation_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    generation_latency_ms: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Sources used for RAG context
    sources_used: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    versions: Mapped[List["DraftVersion"]] = relationship(
        "DraftVersion", back_populates="draft", lazy="select", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Draft id={self.id} type={self.document_type} status={self.status}>"


class DraftVersion(UUIDMixin, Base):
    """
    An immutable version of a draft's content.
    Created on every save/modification — never overwritten.
    """

    __tablename__ = "draft_versions"

    draft_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("drafts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    # AI provenance for this version
    model_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    model_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    generation_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    change_summary: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    draft: Mapped["Draft"] = relationship("Draft", back_populates="versions")
