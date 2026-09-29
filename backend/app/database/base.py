"""
JurisPulse — SQLAlchemy Declarative Base & Mixins
====================================================
All models must inherit from Base.
UUIDMixin and TimestampMixin provide standard columns.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Project-wide declarative base.
    All SQLAlchemy models must inherit from this class.
    Alembic will discover models by importing them via migrations/env.py.
    """
    pass


class UUIDMixin:
    """
    Adds a UUID primary key column.
    Default is generated server-side for portability.
    """

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        nullable=False,
    )


class TimestampMixin:
    """
    Adds created_at and updated_at columns to any model.
    Both are timezone-aware (stored as TIMESTAMPTZ in PostgreSQL).
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    """
    Adds soft-delete support. Records are never physically deleted;
    instead deleted_at is set. Use a query filter to exclude soft-deleted rows.
    """

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
