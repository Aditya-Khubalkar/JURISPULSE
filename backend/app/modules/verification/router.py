"""
JurisPulse — Verification Router
====================================
Routes: /api/v1/verification/*
"""

import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.ai.verification_client import EvidenceItem, VerificationClient, VerificationRequest
from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.database.session import get_db
from app.utils.responses import success_response
from app.modules.verification.models import Approval, VerificationClaim, VerificationResult

verification_router = APIRouter()


class VerifyClaimRequest(BaseModel):
    claim: str = Field(min_length=5, max_length=2000)
    evidence: List[dict] = Field(default_factory=list)


class ApprovalCreate(BaseModel):
    resource_type: str = "DRAFT"
    resource_id: uuid.UUID
    comments: Optional[str] = None


from typing import Optional


@verification_router.post("/check", summary="Verify a claim against evidence")
async def verify_claim(
    body: VerifyClaimRequest,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """
    Run hallucination detection on a claim.
    
    STATUS: Returns NOT_DEPLOYED until the model is trained.
    Confidence is never fabricated.
    """
    client = VerificationClient()
    request = VerificationRequest(
        claim=body.claim,
        evidence=[
            EvidenceItem(
                text=e.get("text", ""),
                source_id=e.get("source_id", ""),
                metadata=e.get("metadata", {}),
            )
            for e in body.evidence
        ],
    )
    result = await client.verify(request)
    return success_response(data={
        "status": result.status,
        "confidence": result.confidence,  # None if NOT_DEPLOYED
        "reason": result.reason,
        "model_used": result.model_used,
        "evidence": result.evidence,
    })


@verification_router.post("/approvals", summary="Request human approval", status_code=201)
async def create_approval(
    body: ApprovalCreate,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Request human review of an AI-generated resource."""
    from datetime import datetime, timezone
    approval = Approval(
        organization_id=current_user.organization_id,
        resource_type=body.resource_type,
        resource_id=body.resource_id,
        requested_by=current_user.id,
        comments=body.comments,
    )
    db.add(approval)
    await db.flush()
    await db.refresh(approval)
    return success_response(
        data={"approval_id": str(approval.id), "status": approval.status},
        message="Approval request created. Awaiting reviewer.",
    )


@verification_router.get("/approvals/{approval_id}", summary="Get approval status")
async def get_approval(
    approval_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Get the status of an approval request."""
    from app.utils.exceptions import NotFoundError
    result = await db.execute(
        select(Approval).where(
            Approval.id == approval_id,
            Approval.organization_id == current_user.organization_id,
        )
    )
    approval = result.scalar_one_or_none()
    if not approval:
        raise NotFoundError("Approval", str(approval_id))
    return success_response(data={
        "id": str(approval.id),
        "resource_type": approval.resource_type,
        "resource_id": str(approval.resource_id),
        "status": approval.status,
        "requested_by": str(approval.requested_by),
        "reviewer_id": str(approval.reviewer_id) if approval.reviewer_id else None,
        "comments": approval.comments,
        "created_at": approval.created_at.isoformat(),
        "resolved_at": approval.resolved_at.isoformat() if approval.resolved_at else None,
    })
