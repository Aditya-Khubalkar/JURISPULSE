"""
JurisPulse — Agent & AgentExecution Models
=============================================
22 logical agents — some deterministic, some LLM-based, some hybrid.
These are NOT 22 separate AI models.

Agents are logical workflow components that may use:
  - Deterministic backend logic
  - RAG retrieval
  - Existing Llama model (via AI Gateway)
  - Embedding model (via AI Gateway)
  - Future models

The distinction between agent type and AI model used is explicit.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config.constants import AgentStatus, AgentType, ExecutionStatus
from app.database.base import Base, TimestampMixin, UUIDMixin


class AgentDefinition(UUIDMixin, TimestampMixin, Base):
    """
    Registry of logical agents available in JurisPulse.
    """

    __tablename__ = "agent_registry"

    agent_id: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    agent_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=AgentType.DETERMINISTIC.value
    )
    version: Mapped[str] = mapped_column(String(50), nullable=False, default="1.0.0")
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=AgentStatus.AVAILABLE.value, index=True
    )
    capabilities: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    required_models: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    is_enabled: Mapped[bool] = mapped_column(default=True, nullable=False)


class AgentExecution(UUIDMixin, Base):
    """
    Records a single agent execution.
    Input/output references point to resource IDs — not raw content.
    """

    __tablename__ = "agent_executions"

    workflow_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    agent_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), nullable=True, index=True
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=ExecutionStatus.PENDING.value
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    duration_ms: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    input_reference: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    output_reference: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    item_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
