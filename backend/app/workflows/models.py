"""
JurisPulse — Workflow Models
================================
Workflow run and state tracking for multi-agent pipelines.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config.constants import WorkflowStatus, WorkflowType
from app.database.base import Base, TimestampMixin, UUIDMixin


class WorkflowRun(UUIDMixin, TimestampMixin, Base):
    """
    A workflow run ties together a sequence of agent executions
    for a given case and workflow type.
    """

    __tablename__ = "workflow_runs"

    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cases.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    workflow_type: Mapped[str] = mapped_column(
        String(100), nullable=False, default=WorkflowType.DOCUMENT_PROCESSING.value
    )
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=WorkflowStatus.QUEUED.value, index=True
    )
    current_stage: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    context_reference: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    completed_agents: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, default=list)
    pending_agents: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, default=list)
    failed_agents: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, default=list)
    approval_required: Mapped[bool] = mapped_column(default=False, nullable=False)
    started_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class WorkflowState(UUIDMixin, Base):
    """Point-in-time state snapshot for a workflow run."""

    __tablename__ = "workflow_states"

    workflow_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("workflow_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    stage: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    state_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(nullable=False)
