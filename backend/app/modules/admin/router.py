"""
JurisPulse — Admin Router
Routes: /api/v1/admin/*
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.ai.health import AIHealthMonitor
from app.modules.agents.registry import AgentRegistryService
from app.modules.auth.dependencies import CurrentUser, require_firm_admin, require_superadmin
from app.modules.auth.models import User
from app.core.config.constants import ModelStatus
from app.database.session import get_db
from app.utils.responses import success_response

admin_router = APIRouter()


@admin_router.get("/ai-status", summary="AI model health status (Admin+)")
async def get_ai_status(
    current_user: User = Depends(CurrentUser),
    _: None = Depends(require_firm_admin()),
):
    """Get health and status of all registered AI models."""
    summary = AIHealthMonitor.get_health_summary()
    return success_response(data=summary)


@admin_router.get("/agents", summary="List all agents (Admin+)")
async def list_all_agents(
    current_user: User = Depends(CurrentUser),
    _: None = Depends(require_firm_admin()),
):
    """List all 22 agents with their status and capabilities."""
    agents = AgentRegistryService.get_all()
    return success_response(
        data=agents,
        meta={"total": len(agents)},
    )


@admin_router.post("/ai-status/refresh", summary="Refresh AI health checks (Admin)")
async def refresh_ai_status(
    current_user: User = Depends(CurrentUser),
    _: None = Depends(require_firm_admin()),
):
    """Force refresh AI service health checks."""
    results = await AIHealthMonitor.check_all()
    return success_response(data=results, message="AI health checks refreshed.")


@admin_router.get("/audit-logs", summary="Query audit logs (Admin)")
async def get_audit_logs(
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_firm_admin()),
    limit: int = 50,
):
    """Query the audit log for the organization."""
    from sqlalchemy import select
    from app.modules.audit.service import AuditLog

    result = await db.execute(
        select(AuditLog)
        .where(AuditLog.organization_id == current_user.organization_id)
        .order_by(AuditLog.timestamp.desc())
        .limit(min(limit, 200))
    )
    logs = result.scalars().all()
    return success_response(data=[
        {
            "id": str(l.id),
            "actor_id": str(l.actor_id) if l.actor_id else None,
            "action": l.action,
            "resource": l.resource,
            "resource_id": l.resource_id,
            "timestamp": l.timestamp.isoformat(),
        }
        for l in logs
    ])
