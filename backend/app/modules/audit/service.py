"""
JurisPulse — Audit Log Model & Service
==========================================
Records all significant system actions for legal compliance.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.constants import AuditAction
from app.database.base import Base, UUIDMixin


class AuditLog(UUIDMixin, Base):
    """Immutable audit log entry. Do NOT add soft delete to this model."""

    __tablename__ = "audit_logs"

    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    actor_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    request_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    log_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)


class AuditService:
    """Records audit log entries."""

    @staticmethod
    async def log(
        db: AsyncSession,
        action: AuditAction,
        actor_id: Optional[uuid.UUID] = None,
        organization_id: Optional[uuid.UUID] = None,
        resource: Optional[str] = None,
        resource_id: Optional[str] = None,
        request_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Create an audit log entry. Non-blocking — does not raise on failure."""
        from datetime import timezone
        try:
            from app.core.config.settings import settings
            if not settings.AUDIT_LOG_ENABLED:
                return
            entry = AuditLog(
                organization_id=organization_id,
                actor_id=actor_id,
                action=action.value if hasattr(action, "value") else action,
                resource=resource,
                resource_id=resource_id,
                request_id=request_id,
                ip_address=ip_address,
                log_metadata=metadata,
                timestamp=datetime.now(timezone.utc),
            )
            db.add(entry)
            await db.flush()
        except Exception:
            pass  # Audit failures must not interrupt business logic
