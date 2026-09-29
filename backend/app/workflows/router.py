"""
JurisPulse — Workflows Router
================================
Routes: /api/v1/workflows/*
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.core.config.constants import WorkflowType
from app.database.session import get_db
from app.utils.exceptions import NotFoundError
from app.utils.responses import created_response, success_response
from app.workflows.models import WorkflowRun

workflows_router = APIRouter()


class WorkflowCreateRequest(BaseModel):
    workflow_type: WorkflowType
    case_id: Optional[uuid.UUID] = None
    context: Optional[dict] = None


@workflows_router.post("", summary="Start a workflow", status_code=201)
async def create_workflow(
    body: WorkflowCreateRequest,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Start a multi-agent workflow for a case."""
    from datetime import datetime, timezone
    run = WorkflowRun(
        organization_id=current_user.organization_id,
        case_id=body.case_id,
        workflow_type=body.workflow_type.value,
        status="QUEUED",
        started_by=current_user.id,
        pending_agents=[],
        completed_agents=[],
        failed_agents=[],
    )
    db.add(run)
    await db.flush()
    await db.refresh(run)
    return created_response(
        data={"workflow_id": str(run.id), "status": run.status, "type": run.workflow_type},
        message="Workflow queued.",
    )


@workflows_router.get("/{workflow_id}", summary="Get workflow status")
async def get_workflow(
    workflow_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Get the current state of a workflow run."""
    result = await db.execute(
        select(WorkflowRun).where(
            WorkflowRun.id == workflow_id,
            WorkflowRun.organization_id == current_user.organization_id,
        )
    )
    run = result.scalar_one_or_none()
    if not run:
        raise NotFoundError("Workflow", str(workflow_id))
    return success_response(data={
        "id": str(run.id),
        "workflow_type": run.workflow_type,
        "status": run.status,
        "current_stage": run.current_stage,
        "completed_agents": run.completed_agents,
        "pending_agents": run.pending_agents,
        "failed_agents": run.failed_agents,
        "approval_required": run.approval_required,
        "created_at": run.created_at.isoformat(),
        "completed_at": run.completed_at.isoformat() if run.completed_at else None,
    })
