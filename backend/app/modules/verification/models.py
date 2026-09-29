"""
JurisPulse — Verification, Citation & Approval Models
========================================================
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config.constants import (
    ApprovalResourceType,
    ApprovalStatus,
    CitationStatus,
    ClaimType,
    VerificationStatus,
)
from app.database.base import Base, TimestampMixin, UUIDMixin


class Citation(UUIDMixin, TimestampMixin, Base):
    """A legal citation extracted from a draft or document."""

    __tablename__ = "citations"

    draft_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("drafts.id", ondelete="SET NULL"), nullable=True, index=True
    )
    document_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )
    citation_text: Mapped[str] = mapped_column(Text, nullable=False)
    case_name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    court: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    section: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    source_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    verification_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=CitationStatus.UNVERIFIED.value
    )
    verified_by_user: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    verified_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)


class VerificationClaim(UUIDMixin, TimestampMixin, Base):
    """A factual claim extracted from a draft for hallucination checking."""

    __tablename__ = "verification_claims"

    draft_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("drafts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    claim_text: Mapped[str] = mapped_column(Text, nullable=False)
    claim_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=ClaimType.FACT.value
    )
    extracted_by: Mapped[str] = mapped_column(
        String(100), nullable=False, default="rule_based"
    )  # "rule_based" or AI model name — NEVER claim AI if not used


class VerificationResult(UUIDMixin, TimestampMixin, Base):
    """
    Result of verifying a claim against retrieved evidence.
    
    IMPORTANT:
    - status=NOT_DEPLOYED when hallucination model is unavailable
    - confidence=None when model not deployed — never fabricated
    """

    __tablename__ = "verification_results"

    claim_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("verification_claims.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=VerificationStatus.NOT_DEPLOYED.value
    )
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # NULL = not computed
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    evidence_used: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class Approval(UUIDMixin, TimestampMixin, Base):
    """
    Human-in-the-loop approval request.
    AI must NOT silently make final legal decisions.
    """

    __tablename__ = "approvals"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    resource_type: Mapped[str] = mapped_column(
        String(100), nullable=False, default=ApprovalResourceType.DRAFT.value
    )
    resource_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    requested_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    reviewer_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=ApprovalStatus.PENDING.value, index=True
    )
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    context: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
