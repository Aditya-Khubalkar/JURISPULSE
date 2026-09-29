"""
JurisPulse — AI Gateway: Legal Drafter Client
================================================
HTTP client for the Llama 3.1 LoRA legal drafting service.
Located at: ai-services/legal-drafter/

Contract:
  POST /generate
  {
    "case_id": "...",
    "document_type": "petition",
    "instructions": "...",
    "case_context": {},
    "sources": []
  }

  Response:
  {
    "text": "...",
    "model": "legal_drafter",
    "model_version": "...",
    "generation_id": "...",
    "metadata": {}
  }
"""

import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import structlog

from app.services.ai.base import AIServiceClient
from app.core.config.settings import settings
from app.utils.exceptions import DraftingServiceError, ModelUnavailableError

logger = structlog.get_logger("jurispulse.ai_gateway.drafter")


@dataclass
class DraftingRequest:
    """Request to the legal drafting service."""

    case_id: str
    document_type: str
    instructions: str
    case_context: Dict[str, Any] = field(default_factory=dict)
    sources: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class DraftingResponse:
    """Response from the legal drafting service."""

    text: str
    model: str
    model_version: str
    generation_id: str
    latency_ms: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class DraftingClient(AIServiceClient):
    """
    Client for the Llama 3.1 LoRA legal drafting service.

    If the service is unavailable, raises ModelUnavailableError — never
    returns a fake draft or a draft from a different model.
    """

    def __init__(self) -> None:
        super().__init__(
            base_url=settings.AI_DRAFTER_URL,
            timeout=settings.AI_SERVICE_TIMEOUT,
        )

    async def generate_draft(self, request: DraftingRequest) -> DraftingResponse:
        """
        Call the Llama 3.1 drafting service to generate a legal document.

        Raises:
            ModelUnavailableError: If the service is offline or not responding.
            DraftingServiceError: If the service returns an error response.
        """
        from app.services.ai.registry import AIModelRegistryService
        if not AIModelRegistryService.is_available("legal_drafter"):
            raise ModelUnavailableError("Llama 3.1 legal drafter")

        import time
        start = time.perf_counter()

        try:
            response = await self._post(
                "/generate",
                {
                    "case_id": request.case_id,
                    "document_type": request.document_type,
                    "instructions": request.instructions,
                    "case_context": request.case_context,
                    "sources": request.sources,
                },
            )
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
        except Exception as e:
            logger.error(
                "drafter_client.failed",
                document_type=request.document_type,
                error=str(e),
            )
            raise DraftingServiceError(f"Legal drafter service failed: {e}")

        # Validate response has required fields
        if not response.get("text"):
            raise DraftingServiceError("Drafting service returned empty text.")

        return DraftingResponse(
            text=response["text"],
            model=response.get("model", "legal_drafter"),
            model_version=response.get("model_version", "unknown"),
            generation_id=response.get("generation_id", str(uuid.uuid4())),
            latency_ms=latency_ms,
            metadata=response.get("metadata", {}),
        )
