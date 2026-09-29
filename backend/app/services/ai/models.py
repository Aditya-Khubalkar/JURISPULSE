"""
JurisPulse — AI Model Registry (Database Model)
==================================================
Persists AI model registrations so they can be queried via the admin API.
"""

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Float, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config.constants import ModelStatus, ModelType
from app.database.base import Base, TimestampMixin, UUIDMixin


class AIModelRegistry(UUIDMixin, TimestampMixin, Base):
    """
    Registry of all AI models known to the system.
    Includes both deployed and NOT_DEPLOYED models.
    """

    __tablename__ = "model_registry"

    model_id: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )  # e.g. "legal_drafter", "embedding_model", "hallucination_detector"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    model_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=ModelType.LLM.value
    )
    purpose: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    endpoint: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=ModelStatus.NOT_DEPLOYED.value, index=True
    )
    health_status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=ModelStatus.NOT_DEPLOYED.value
    )
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    timeout_seconds: Mapped[int] = mapped_column(Integer, default=120, nullable=False)
    last_health_check_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    last_latency_ms: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    capabilities: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<AIModelRegistry model_id={self.model_id} status={self.status}>"
