"""
JurisPulse — Hearings Router
Routes: /api/v1/hearings/*
"""

import uuid
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.database.session import get_db
from app.modules.timeline.models import Hearing
from app.utils.responses import created_response, success_response

hearings_router = APIRouter()


class HearingCreate(BaseModel):
    case_id: uuid.UUID
    hearing_date: datetime
    court: Optional[str] = None
    purpose: Optional[str] = None


@hearings_router.post("", summary="Schedule hearing", status_code=201)
async def create_hearing(
    body: HearingCreate,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    hearing = Hearing(
        organization_id=current_user.organization_id,
        case_id=body.case_id,
        hearing_date=body.hearing_date,
        court=body.court,
        purpose=body.purpose,
        status="SCHEDULED",
        created_by=current_user.id,
    )
    db.add(hearing)
    await db.flush()
    await db.refresh(hearing)
    return created_response(data={"id": str(hearing.id), "hearing_date": str(hearing.hearing_date)})


@hearings_router.get("/case/{case_id}", summary="List hearings for case")
async def list_hearings(
    case_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Hearing)
        .where(
            Hearing.case_id == case_id,
            Hearing.organization_id == current_user.organization_id,
        )
        .order_by(Hearing.hearing_date)
    )
    hearings = result.scalars().all()
    return success_response(data=[
        {
            "id": str(h.id),
            "hearing_date": str(h.hearing_date),
            "court": h.court,
            "purpose": h.purpose,
            "status": h.status,
            "outcome": h.outcome,
        }
        for h in hearings
    ])
