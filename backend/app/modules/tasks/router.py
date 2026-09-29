"""
JurisPulse — Tasks Router
Routes: /api/v1/tasks/*
"""

import uuid
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.core.config.constants import Priority
from app.database.session import get_db
from app.modules.timeline.models import Task
from app.utils.responses import created_response, success_response

tasks_router = APIRouter()


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=500)
    description: Optional[str] = None
    case_id: Optional[uuid.UUID] = None
    assigned_to: Optional[uuid.UUID] = None
    priority: Priority = Priority.MEDIUM
    due_date: Optional[date] = None


@tasks_router.post("", summary="Create task", status_code=201)
async def create_task(
    body: TaskCreate,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    task = Task(
        organization_id=current_user.organization_id,
        case_id=body.case_id,
        title=body.title,
        description=body.description,
        assigned_to=body.assigned_to,
        created_by=current_user.id,
        status="PENDING",
        priority=body.priority.value,
        due_date=body.due_date,
    )
    db.add(task)
    await db.flush()
    await db.refresh(task)
    return created_response(data={"id": str(task.id), "title": task.title, "status": task.status})


@tasks_router.get("/my", summary="Get my tasks")
async def get_my_tasks(
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Task).where(
            Task.assigned_to == current_user.id,
            Task.organization_id == current_user.organization_id,
            Task.status != "COMPLETED",
        ).order_by(Task.due_date.asc().nullsfirst())
    )
    tasks = result.scalars().all()
    return success_response(data=[
        {
            "id": str(t.id),
            "title": t.title,
            "status": t.status,
            "priority": t.priority,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "case_id": str(t.case_id) if t.case_id else None,
        }
        for t in tasks
    ])
