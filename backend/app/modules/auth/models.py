"""
JurisPulse — Auth & User Models
==================================
SQLAlchemy models for users and refresh tokens.

Authentication authority: Supabase Auth.
- Users authenticate via Supabase Auth, which issues JWTs.
- This backend verifies those JWTs and maps them to local User records.
- Local User records store application-level profile data.
- We do NOT create a second conflicting password-based auth system.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.modules.organizations.models import Organization
    from app.modules.roles.models import UserRole as UserRoleAssoc


class User(UUIDMixin, TimestampMixin, Base):
    """
    Application user record.

    The primary identity is the Supabase Auth user (supabase_user_id).
    This record stores additional application-level profile data.

    IMPORTANT: email / auth is managed by Supabase. Do not duplicate
    password hashing here — it would create a split-brain auth situation.
    """

    __tablename__ = "users"

    # Supabase Auth user ID (sub claim in JWT)
    supabase_user_id: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    email: Mapped[str] = mapped_column(
        String(320), unique=True, nullable=False, index=True
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Organization this user belongs to (nullable for super-admin)
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    last_login_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_login_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)

    # Relationships
    organization: Mapped[Optional["Organization"]] = relationship(
        "Organization", back_populates="users", lazy="select"
    )
    role_assignments: Mapped[List["UserRoleAssoc"]] = relationship(
        "UserRole", back_populates="user", lazy="select", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"


class RefreshToken(UUIDMixin, Base):
    """
    Stored refresh tokens for token rotation.
    Used only if locally issued refresh tokens are needed (e.g., Celery callbacks).
    Supabase manages its own refresh tokens separately.
    """

    __tablename__ = "refresh_tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["User"] = relationship("User", lazy="select")
