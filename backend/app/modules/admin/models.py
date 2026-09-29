"""
JurisPulse — Admin Models (Dataset registry placeholder)
"""

import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base, TimestampMixin, UUIDMixin


class Dataset(UUIDMixin, TimestampMixin, Base):
    """Placeholder for admin-managed datasets (training data, glossaries, etc.)"""

    __tablename__ = "datasets"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    dataset_type: Mapped[str] = mapped_column(String(100), nullable=False, default="TRAINING_DATA")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="DRAFT")
