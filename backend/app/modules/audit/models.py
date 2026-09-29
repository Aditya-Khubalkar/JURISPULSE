"""
JurisPulse — Audit Log Model (imported separately for Alembic)
"""
from app.modules.audit.service import AuditLog  # re-export

__all__ = ["AuditLog"]
