"""
JurisPulse — AI Gateway: Hallucination Verification Client
============================================================
HTTP client for the hallucination detection service.
Located at: ai-services/hallucination-detector/

STATUS: NOT_DEPLOYED
The hallucination detection model has NOT been trained yet.
This client is the infrastructure for when it is deployed.

Until the model is deployed:
  - All verify() calls return status="NOT_DEPLOYED"
  - No fake confidence values are returned
  - No fake verification results are fabricated

Contract:
  POST /verify
  {
    "claim": "...",
    "evidence": [{"text": "...", "source_id": "...", "metadata": {}}]
  }

  Response:
  {
    "status": "SUPPORTED" | "PARTIALLY_SUPPORTED" | "UNSUPPORTED" |
              "CONTRADICTED" | "UNVERIFIED" | "NOT_DEPLOYED",
    "confidence": 0.94,
    "reason": "...",
    "evidence": []
  }
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import structlog

from app.services.ai.base import AIServiceClient
from app.core.config.constants import VerificationStatus
from app.core.config.settings import settings

logger = structlog.get_logger("jurispulse.ai_gateway.verification")


@dataclass
class EvidenceItem:
    text: str
    source_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VerificationRequest:
    claim: str
    evidence: List[EvidenceItem] = field(default_factory=list)


@dataclass
class VerificationResponse:
    """
    Response from the hallucination detection service.

    IMPORTANT:
    - confidence is None when model is NOT_DEPLOYED — not fabricated
    - status is "NOT_DEPLOYED" until the model is actually trained
    """

    status: str  # VerificationStatus value
    confidence: Optional[float]  # None if NOT_DEPLOYED
    reason: str
    evidence: List[Dict] = field(default_factory=list)
    model_used: Optional[str] = None


class VerificationClient(AIServiceClient):
    """
    Client for the hallucination detection service.

    Behaviour when model is NOT_DEPLOYED:
      - Returns VerificationResponse with status=NOT_DEPLOYED
      - confidence=None (never fabricated)
      - Does NOT call the service (it doesn't exist yet)
    """

    def __init__(self) -> None:
        super().__init__(
            base_url=settings.AI_VERIFICATION_URL,
            timeout=settings.AI_SERVICE_TIMEOUT,
        )

    async def verify(self, request: VerificationRequest) -> VerificationResponse:
        """
        Verify a claim against provided evidence.

        Returns NOT_DEPLOYED status until the model is trained and deployed.
        """
        from app.services.ai.registry import AIModelRegistryService
        model = AIModelRegistryService.get("hallucination_detector")

        if model is None or not model.is_enabled:
            # Model is NOT_DEPLOYED — return honest status, not fabricated result
            return VerificationResponse(
                status=VerificationStatus.NOT_DEPLOYED.value,
                confidence=None,  # NEVER fabricate a confidence score
                reason=(
                    "Hallucination detection model is not yet deployed. "
                    "This claim has not been verified."
                ),
                model_used=None,
            )

        try:
            response = await self._post(
                "/verify",
                {
                    "claim": request.claim,
                    "evidence": [
                        {
                            "text": e.text,
                            "source_id": e.source_id,
                            "metadata": e.metadata,
                        }
                        for e in request.evidence
                    ],
                },
            )
            return VerificationResponse(
                status=response.get("status", VerificationStatus.UNVERIFIED.value),
                confidence=response.get("confidence"),  # Could be None from service
                reason=response.get("reason", ""),
                evidence=response.get("evidence", []),
                model_used=response.get("model", "hallucination_detector"),
            )
        except Exception as e:
            logger.warning("verification_client.failed", error=str(e))
            # Service error — return UNVERIFIED, not fabricated confidence
            return VerificationResponse(
                status=VerificationStatus.UNVERIFIED.value,
                confidence=None,
                reason=f"Verification service unavailable: {e}",
                model_used=None,
            )
