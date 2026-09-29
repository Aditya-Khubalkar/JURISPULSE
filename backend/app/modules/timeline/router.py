"""
JurisPulse — Timeline Router
Routes: /api/v1/timeline/*
"""

import uuid
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.database.session import get_db
from app.modules.timeline.models import TimelineEvent
from app.utils.responses import created_response, success_response

timeline_router = APIRouter()


class TimelineEventCreate(BaseModel):
    case_id: uuid.UUID
    event_date: date
    title: str = Field(min_length=2, max_length=500)
    description: Optional[str] = None
    event_type: str = "GENERAL"


@timeline_router.post("", summary="Add timeline event", status_code=201)
async def create_event(
    body: TimelineEventCreate,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    event = TimelineEvent(
        organization_id=current_user.organization_id,
        case_id=body.case_id,
        event_date=body.event_date,
        title=body.title,
        description=body.description,
        event_type=body.event_type,
        is_ai_extracted=False,
        created_by=current_user.id,
    )
    db.add(event)
    await db.flush()
    await db.refresh(event)
    return created_response(data={"id": str(event.id), "title": event.title})


@timeline_router.get("/{case_id}", summary="Get case timeline")
async def get_timeline(
    case_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(TimelineEvent)
        .where(
            TimelineEvent.case_id == case_id,
            TimelineEvent.organization_id == current_user.organization_id,
        )
        .order_by(TimelineEvent.event_date)
    )
    events = result.scalars().all()
    return success_response(data=[
        {
            "id": str(e.id),
            "event_date": e.event_date.isoformat(),
            "title": e.title,
            "description": e.description,
            "event_type": e.event_type,
            "is_ai_extracted": e.is_ai_extracted,
        }
        for e in events
    ])
