"""
JurisPulse — Drafting Service
================================
Orchestrates the 13-step legal draft generation workflow:

  1. Authenticate user
  2. Verify case access
  3. Load case information
  4. Load selected documents
  5. Retrieve relevant precedents (RAG)
  6. Build drafting context
  7. Call legal_drafter AI service (Llama 3.1 LoRA)
  8. Save generated draft
  9. Store model/version metadata
 10. Extract claims for verification (placeholder)
 11. If verification deployed, run verification
 12. If critical review required, create approval
 13. Return draft and provenance

IMPORTANT:
  - Do NOT claim a draft was AI-generated if the model was not actually called
  - If Llama is unavailable, return ModelUnavailableError (not a fake draft)
  - Store ALL provenance: model, version, generation_id, latency
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.ai.drafting_client import DraftingClient, DraftingRequest
from app.modules.cases.repository import CaseRepository
from app.modules.drafting.models import Draft, DraftVersion
from app.core.config.constants import (
    AuditAction,
    DocumentType,
    DraftGenerationType,
    DraftStatus,
)
from app.modules.research.service import ResearchService
from app.utils.exceptions import (
    CaseAccessDeniedError,
    CaseNotFoundError,
    ModelUnavailableError,
)

logger = structlog.get_logger("jurispulse.drafting.service")


class DraftingService:
    """Orchestrates the full legal draft generation workflow."""

    @staticmethod
    async def generate_draft(
        db: AsyncSession,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        case_id: uuid.UUID,
        document_type: str,
        instructions: str,
        title: Optional[str] = None,
        research_limit: int = 5,
    ) -> Dict[str, Any]:
        """
        Execute the full drafting workflow.
        Returns the draft with full AI provenance metadata.
        """
        # --- Step 2: Verify case access ---
        case = await CaseRepository.get_by_id(db, case_id, organization_id)
        if not case:
            raise CaseNotFoundError(str(case_id))
        member = await CaseRepository.get_member(db, case_id, user_id)
        if not member:
            raise CaseAccessDeniedError()

        # --- Step 3 + 4: Build case context ---
        case_context = {
            "case_number": case.case_number,
            "title": case.title,
            "case_type": case.case_type,
            "court": case.court,
            "jurisdiction": case.jurisdiction,
            "filing_date": str(case.filing_date) if case.filing_date else None,
        }

        # --- Step 5: Retrieve relevant precedents ---
        sources = []
        try:
            research_result = await ResearchService.search(
                db=db,
                query_text=f"{document_type} {instructions}",
                organization_id=organization_id,
                user_id=user_id,
                case_id=case_id,
                limit=research_limit,
            )
            if research_result.get("status") == "COMPLETED":
                sources = [
                    {
                        "text": r["text"],
                        "source_id": r.get("source_id"),
                        "similarity": r["similarity_score"],
                    }
                    for r in research_result.get("results", [])
                    if r.get("is_relevant")
                ]
        except Exception as e:
            logger.warning("drafting.retrieval_failed", error=str(e))
            # Proceed with empty sources — don't block drafting

        # --- Step 7: Call the legal drafter AI service ---
        try:
            client = DraftingClient()
            ai_response = await client.generate_draft(
                DraftingRequest(
                    case_id=str(case_id),
                    document_type=document_type,
                    instructions=instructions,
                    case_context=case_context,
                    sources=sources,
                )
            )
        except ModelUnavailableError:
            raise  # Propagate — don't pretend to have a draft

        # --- Step 8 + 9: Save draft with full provenance ---
        draft_title = title or f"{document_type.replace('_', ' ').title()} — {case.title[:50]}"
        draft = Draft(
            organization_id=organization_id,
            case_id=case_id,
            title=draft_title,
            document_type=document_type,
            status=DraftStatus.DRAFT.value,
            generation_type=DraftGenerationType.AI_GENERATED.value,
            created_by=user_id,
            instructions=instructions,
            model_name=ai_response.model,
            model_version=ai_response.model_version,
            generation_id=ai_response.generation_id,
            generation_latency_ms=ai_response.latency_ms,
            sources_used={"count": len(sources), "sources": sources[:5]},  # Don't store full text
        )
        db.add(draft)
        await db.flush()

        # Create initial version
        version = DraftVersion(
            draft_id=draft.id,
            version_number=1,
            content=ai_response.text,
            created_by=user_id,
            created_at=datetime.now(timezone.utc),
            model_name=ai_response.model,
            model_version=ai_response.model_version,
            generation_id=ai_response.generation_id,
        )
        db.add(version)
        await db.flush()

        # Audit log
        from app.modules.audit.service import AuditService
        await AuditService.log(
            db,
            actor_id=user_id,
            organization_id=organization_id,
            action=AuditAction.DRAFT_GENERATE,
            resource="drafts",
            resource_id=str(draft.id),
            metadata={
                "document_type": document_type,
                "model": ai_response.model,
                "model_version": ai_response.model_version,
                "sources_used": len(sources),
            },
        )

        logger.info(
            "draft.generated",
            draft_id=str(draft.id),
            model=ai_response.model,
            latency_ms=ai_response.latency_ms,
        )

        return {
            "draft_id": str(draft.id),
            "title": draft.title,
            "document_type": draft.document_type,
            "status": draft.status,
            "version": 1,
            "content": ai_response.text,
            "provenance": {
                "model": ai_response.model,
                "model_version": ai_response.model_version,
                "generation_id": ai_response.generation_id,
                "latency_ms": ai_response.latency_ms,
                "sources_used": len(sources),
            },
            "verification_status": "NOT_DEPLOYED",
            "requires_human_review": True,
            "message": (
                "Draft generated by AI. This content must be reviewed by a qualified "
                "legal professional before use. AI-generated content may contain errors."
            ),
        }
