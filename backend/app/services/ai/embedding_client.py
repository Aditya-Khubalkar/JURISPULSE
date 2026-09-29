"""
JurisPulse — AI Gateway: Embedding Client
============================================
HTTP client for the bge-small embedding service.
Located at: ai-services/embeddings/

The backend calls this client; the embedding service loads the actual model.
The backend NEVER imports sentence-transformers, torch, or similar here.
"""

from dataclasses import dataclass, field
from typing import List

import structlog

from app.services.ai.base import AIServiceClient
from app.core.config.settings import settings
from app.utils.exceptions import EmbeddingServiceError, ModelUnavailableError

logger = structlog.get_logger("jurispulse.ai_gateway.embedding")


@dataclass
class EmbeddingResponse:
    """Response from the embedding service."""

    model: str
    embeddings: List[List[float]]
    token_count: int = 0
    latency_ms: float = 0.0


class EmbeddingClient(AIServiceClient):
    """
    Client for the bge-small embedding service.
    
    Usage::
        client = EmbeddingClient()
        response = await client.embed(texts=["query text"])
        embeddings = response.embeddings  # List[List[float]]
    """

    def __init__(self) -> None:
        super().__init__(
            base_url=settings.AI_EMBEDDING_URL,
            timeout=60,
        )

    async def embed(self, texts: List[str]) -> EmbeddingResponse:
        """
        Embed a list of texts.
        Returns a list of embedding vectors (one per input text).
        Raises ModelUnavailableError if the service is unreachable.
        """
        if not texts:
            return EmbeddingResponse(model="embedding_model", embeddings=[])

        # Validate that service is available via registry
        from app.services.ai.registry import AIModelRegistryService
        if not AIModelRegistryService.is_available("embedding_model"):
            raise ModelUnavailableError("bge-small embedding service")

        try:
            import time
            start = time.perf_counter()
            response = await self._post("/embed", {"texts": texts})
            latency_ms = round((time.perf_counter() - start) * 1000, 2)

            return EmbeddingResponse(
                model=response.get("model", "embedding_model"),
                embeddings=response.get("embeddings", []),
                token_count=response.get("token_count", 0),
                latency_ms=latency_ms,
            )
        except Exception as e:
            logger.error("embedding_client.failed", error=str(e), text_count=len(texts))
            raise EmbeddingServiceError(f"Embedding service failed: {e}")

    async def embed_query(self, query: str) -> List[float]:
        """Embed a single query text. Returns the embedding vector."""
        response = await self.embed([query])
        if response.embeddings:
            return response.embeddings[0]
        raise EmbeddingServiceError("No embedding returned for query.")
