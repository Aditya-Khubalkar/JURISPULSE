"""
JurisPulse — Organization Model
==================================
Multi-tenant organization — every case, user, and resource belongs to one.
"""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.modules.auth.models import User
    from app.modules.cases.models import Case
    from app.modules.clients.models import Client


class Organization(UUIDMixin, TimestampMixin, Base):
    """
    A law firm or legal department.

    Every data entity in JurisPulse (cases, documents, drafts, etc.)
    is scoped to an organization. Cross-organization data access is
    prevented at the service layer — NEVER trust organization_id from
    the request body.
    """

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    # Contact information
    email: Mapped[Optional[str]] = mapped_column(String(320), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100), default="India", nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    max_users: Mapped[int] = mapped_column(default=50, nullable=False)

    # Relationships
    users: Mapped[List["User"]] = relationship(
        "User", back_populates="organization", lazy="select"
    )

    def __repr__(self) -> str:
        return f"<Organization id={self.id} name={self.name}>"
