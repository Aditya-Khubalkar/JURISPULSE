"""
JurisPulse — Health Check Endpoint
=====================================
Simple health and readiness endpoints consumed by:
- Docker health checks
- Kubernetes liveness / readiness probes
- Frontend connectivity checks
- AI Gateway availability polling
"""

import time
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db

health_router = APIRouter()

_START_TIME = time.time()


@health_router.get(
    "/health",
    summary="Basic health check",
    description="Returns 200 if the backend process is running.",
    response_description="Service status",
)
async def health_check() -> dict[str, Any]:
    """Basic liveness probe — just checks the process is alive."""
    return {
        "success": True,
        "data": {
            "status": "ok",
            "service": "jurispulse-backend",
            "uptime_seconds": round(time.time() - _START_TIME, 1),
        },
        "message": "Service is running.",
    }


@health_router.get(
    "/ready",
    summary="Readiness check",
    description="Checks that the database connection is available.",
    response_description="Readiness status",
)
async def readiness_check(db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    """
    Readiness probe.
    Verifies that the PostgreSQL connection pool can execute a query.
    Returns 503 if the database is unreachable.
    """
    db_ok = False
    db_error: str | None = None
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception as e:
        db_error = str(e)

    status = "ready" if db_ok else "not_ready"
    http_status = 200 if db_ok else 503

    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=http_status,
        content={
            "success": db_ok,
            "data": {
                "status": status,
                "checks": {
                    "database": "ok" if db_ok else f"error: {db_error}",
                },
            },
            "message": "Service is ready." if db_ok else "Service is not ready.",
        },
    )
