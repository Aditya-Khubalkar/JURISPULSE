"""
JurisPulse — Shared API Dependencies
=======================================
Common FastAPI dependencies used across all route modules.

These are imported by individual routers — not by main.py directly.
"""

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.settings import settings
from app.database.session import get_db

# Re-export the database dependency with a typed alias
DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


async def get_request_id(x_request_id: str | None = Header(default=None)) -> str | None:
    """Extract the X-Request-ID header (injected by RequestIDMiddleware)."""
    return x_request_id


RequestIDDep = Annotated[str | None, Depends(get_request_id)]


async def verify_internal_token(
    x_internal_token: str | None = Header(default=None),
) -> None:
    """
    Lightweight token for internal service-to-service calls.
    Not a substitute for user authentication — used for health aggregators,
    Celery result callbacks, etc.
    """
    if x_internal_token != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid internal service token.",
        )
