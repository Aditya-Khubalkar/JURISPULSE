"""
JurisPulse — Evidence Router
================================
Routes: /api/v1/evidence/*
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.database.session import get_db
from app.modules.evidence.models import Evidence
from app.utils.exceptions import NotFoundError
from app.utils.responses import created_response, success_response

evidence_router = APIRouter()


class EvidenceCreate(BaseModel):
    case_id: uuid.UUID
    title: str = Field(min_length=2, max_length=500)
    description: Optional[str] = None
    evidence_type: str = "DOCUMENTARY"
    source: Optional[str] = None
    document_id: Optional[uuid.UUID] = None


class EvidenceRead(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    case_id: uuid.UUID
    document_id: Optional[uuid.UUID]
    title: str
    description: Optional[str]
    evidence_type: str
    source: Optional[str]
    is_ai_extracted: bool


@evidence_router.post("", summary="Add evidence item", status_code=201)
async def create_evidence(
    body: EvidenceCreate,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    evidence = Evidence(
        organization_id=current_user.organization_id,
        case_id=body.case_id,
        document_id=body.document_id,
        title=body.title,
        description=body.description,
        evidence_type=body.evidence_type,
        source=body.source,
        is_ai_extracted=False,
        added_by=current_user.id,
    )
    db.add(evidence)
    await db.flush()
    await db.refresh(evidence)
    return created_response(data=EvidenceRead.model_validate(evidence).model_dump())


@evidence_router.get("/{evidence_id}", summary="Get evidence by ID")
async def get_evidence(
    evidence_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Evidence).where(
            Evidence.id == evidence_id,
            Evidence.organization_id == current_user.organization_id,
        )
    )
    ev = result.scalar_one_or_none()
    if not ev:
        raise NotFoundError("Evidence", str(evidence_id))
    return success_response(data=EvidenceRead.model_validate(ev).model_dump())
