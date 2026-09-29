"""
JurisPulse — Agents Router
=============================
Routes: /api/v1/agents/*
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.agents.registry import AgentRegistryService
from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.database.session import get_db
from app.utils.exceptions import NotFoundError
from app.utils.responses import success_response

agents_router = APIRouter()


@agents_router.get("", summary="List all agents")
async def list_agents(
    current_user: User = Depends(CurrentUser),
    status: Optional[str] = None,
):
    """List all registered agents with their current status."""
    agents = AgentRegistryService.get_all()
    if status:
        agents = [a for a in agents if a["status"] == status.upper()]
    return success_response(
        data=agents,
        meta={"total": len(agents)},
    )


@agents_router.get("/{agent_id}", summary="Get agent details")
async def get_agent(
    agent_id: str,
    current_user: User = Depends(CurrentUser),
):
    """Get details for a specific agent."""
    agent = AgentRegistryService.get(agent_id)
    if not agent:
        raise NotFoundError("Agent", agent_id)
    return success_response(data=agent)


@agents_router.get("/executions/list", summary="List agent executions")
async def list_executions(
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
    case_id: Optional[uuid.UUID] = None,
):
    """List recent agent executions for the organization."""
    from sqlalchemy import select
    from app.modules.agents.models import AgentExecution

    query = select(AgentExecution).where(
        AgentExecution.organization_id == current_user.organization_id
    )
    if case_id:
        query = query.where(AgentExecution.case_id == case_id)
    result = await db.execute(query.order_by(AgentExecution.started_at.desc()).limit(50))
    executions = result.scalars().all()
    return success_response(data=[
        {
            "id": str(e.id),
            "agent_id": e.agent_id,
            "case_id": str(e.case_id) if e.case_id else None,
            "status": e.status,
            "model_used": e.model_used,
            "duration_ms": e.duration_ms,
            "started_at": e.started_at.isoformat() if e.started_at else None,
        }
        for e in executions
    ])
