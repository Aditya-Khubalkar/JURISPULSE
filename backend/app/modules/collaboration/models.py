"""Re-export Comment and CaseMention models."""
from app.modules.timeline.models import CaseMention, Comment  # noqa
__all__ = ["Comment", "CaseMention"]
