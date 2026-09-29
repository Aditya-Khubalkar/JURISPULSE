"""
JurisPulse — Case, CaseParty, CaseMember Models
==================================================
Core case management models.

Key design decisions:
- organization_id is always set from the authenticated user, never from request body
- Case numbers are stored as provided (Indian courts use various formats)
- Multiple parties can belong to one case
- Multiple firm members can be assigned to one case with different roles
"""

import uuid
from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config.constants import (
    CaseMemberRole,
    CaseStatus,
    CaseType,
    PartyType,
    Priority,
)
from app.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.modules.clients.models import Client
    from app.modules.auth.models import User
    from app.modules.documents.models import Document
    from app.modules.timeline.models import TimelineEvent
    from app.modules.hearings.models import Hearing


class Case(UUIDMixin, TimestampMixin, Base):
    """
    A legal case or matter managed by the organization.
    """

    __tablename__ = "cases"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    case_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    case_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=CaseType.CIVIL.value, index=True
    )
    court: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    jurisdiction: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    filing_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=CaseStatus.OPEN.value, index=True
    )
    priority: Mapped[str] = mapped_column(
        String(20), nullable=False, default=Priority.MEDIUM.value
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_confidential: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    client_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )

    # Extra structured metadata (acts involved, relief sought, etc.)
    item_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, default=dict)

    # Relationships
    parties: Mapped[List["CaseParty"]] = relationship(
        "CaseParty", back_populates="case", lazy="select", cascade="all, delete-orphan"
    )
    members: Mapped[List["CaseMember"]] = relationship(
        "CaseMember", back_populates="case", lazy="select", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Case id={self.id} number={self.case_number} status={self.status}>"


class CaseParty(UUIDMixin, TimestampMixin, Base):
    """
    A party involved in the case (petitioner, respondent, etc.)
    Multiple parties of different types can exist per case.
    """

    __tablename__ = "case_parties"

    case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    party_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=PartyType.PETITIONER.value
    )
    role: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    advocate_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_information: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    item_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    case: Mapped["Case"] = relationship("Case", back_populates="parties")


class CaseMember(UUIDMixin, Base):
    """
    Assigns a firm user (lawyer, paralegal, etc.) to a case.
    Controls who can access the case and in what capacity.
    """

    __tablename__ = "case_members"

    case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(
        String(50), nullable=False, default=CaseMemberRole.ASSOCIATE.value
    )
    is_lead: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    added_by: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    added_at: Mapped[datetime] = mapped_column(
        nullable=False
    )

    case: Mapped["Case"] = relationship("Case", back_populates="members")

    __table_args__ = (
        UniqueConstraint("case_id", "user_id", name="uq_case_member"),
    )
