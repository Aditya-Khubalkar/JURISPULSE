"""
Re-export Hearing model from timeline domain models for Alembic.
"""
from app.modules.timeline.models import Hearing  # noqa

__all__ = ["Hearing"]
