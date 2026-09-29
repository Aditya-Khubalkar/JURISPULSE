"""
JurisPulse — Drafting Router
================================
Routes: /api/v1/drafts/*
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.core.config.constants import DocumentType
from app.database.session import get_db
from app.modules.drafting.models import Draft, DraftVersion
from app.modules.drafting.service import DraftingService
from app.utils.exceptions import NotFoundError
from app.utils.responses import created_response, success_response

drafting_router = APIRouter()


class GenerateDraftRequest(BaseModel):
    case_id: uuid.UUID
    document_type: DocumentType
    instructions: str = Field(min_length=10, max_length=5000)
    title: Optional[str] = Field(default=None, max_length=500)
    research_limit: int = Field(default=5, ge=1, le=20)


@drafting_router.post(
    "/generate",
    summary="Generate a legal draft using AI",
    status_code=201,
)
async def generate_draft(
    body: GenerateDraftRequest,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate a legal draft using the Llama 3.1 LoRA model.
    
    IMPORTANT:
    - If the AI model is unavailable, returns 503 (not a fake draft)
    - All drafts must be reviewed by a qualified legal professional
    - AI provenance (model, version, generation ID) is always returned
    """
    result = await DraftingService.generate_draft(
        db=db,
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        case_id=body.case_id,
        document_type=body.document_type.value,
        instructions=body.instructions,
        title=body.title,
        research_limit=body.research_limit,
    )
    return created_response(data=result, message=result.get("message", "Draft generated."))


@drafting_router.get("", summary="List drafts")
async def list_drafts(
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
    case_id: Optional[uuid.UUID] = None,
):
    """List all drafts accessible to the current user."""
    query = select(Draft).where(Draft.organization_id == current_user.organization_id)
    if case_id:
        query = query.where(Draft.case_id == case_id)
    result = await db.execute(query.order_by(Draft.created_at.desc()).limit(50))
    drafts = result.scalars().all()
    return success_response(data=[
        {
            "id": str(d.id),
            "title": d.title,
            "document_type": d.document_type,
            "status": d.status,
            "case_id": str(d.case_id),
            "model_name": d.model_name,
            "current_version": d.current_version,
            "created_at": d.created_at.isoformat(),
        }
        for d in drafts
    ])


@drafting_router.get("/{draft_id}", summary="Get draft with latest version")
async def get_draft(
    draft_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Get a draft including its latest content."""
    result = await db.execute(
        select(Draft).where(
            Draft.id == draft_id,
            Draft.organization_id == current_user.organization_id,
        )
    )
    draft = result.scalar_one_or_none()
    if not draft:
        raise NotFoundError("Draft", str(draft_id))

    # Get latest version
    v_result = await db.execute(
        select(DraftVersion)
        .where(DraftVersion.draft_id == draft_id)
        .order_by(DraftVersion.version_number.desc())
        .limit(1)
    )
    latest_version = v_result.scalar_one_or_none()

    return success_response(data={
        "id": str(draft.id),
        "title": draft.title,
        "document_type": draft.document_type,
        "status": draft.status,
        "case_id": str(draft.case_id),
        "current_version": draft.current_version,
        "content": latest_version.content if latest_version else None,
        "provenance": {
            "model": draft.model_name,
            "model_version": draft.model_version,
            "generation_id": draft.generation_id,
            "latency_ms": draft.generation_latency_ms,
        },
        "created_at": draft.created_at.isoformat(),
    })
