"""
JurisPulse — Client Model
===========================
A client is the person/entity the law firm represents.
"""

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config.constants import ClientType
from app.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.modules.organizations.models import Organization
    from app.modules.cases.models import Case


class Client(UUIDMixin, TimestampMixin, Base):
    """
    A client (individual or corporate) that the organization represents.
    Clients are scoped to the organization — never cross-tenant accessible.
    """

    __tablename__ = "clients"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(320), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    client_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=ClientType.INDIVIDUAL.value
    )
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True
    )

    def __repr__(self) -> str:
        return f"<Client id={self.id} name={self.name}>"
