"""
JurisPulse — AI Gateway: Abstract Base Client
================================================
All AI service clients inherit from this base.
The backend NEVER imports torch, transformers, or model weights here.
It only makes HTTP calls to independently running AI services.
"""

import abc
import time
from typing import Any, Optional

import httpx
import structlog

from app.core.config.settings import settings

logger = structlog.get_logger("jurispulse.ai_gateway")


class AIServiceClient(abc.ABC):
    """
    Abstract base class for all AI service HTTP clients.

    Subclasses must implement the service-specific methods.
    All communication is over HTTP to a separately running service.
    Unavailability is handled gracefully — services can be offline
    without crashing the backend.
    """

    def __init__(self, base_url: str, timeout: int = settings.AI_SERVICE_TIMEOUT) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(self.timeout),
                headers={"Content-Type": "application/json"},
            )
        return self._client

    async def _post(self, endpoint: str, payload: dict) -> dict:
        """Make a POST request to the AI service. Returns parsed JSON."""
        client = await self._get_client()
        start = time.perf_counter()
        try:
            response = await client.post(endpoint, json=payload)
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            response.raise_for_status()
            logger.debug(
                "ai_gateway.response",
                endpoint=endpoint,
                status=response.status_code,
                latency_ms=latency_ms,
            )
            return response.json()
        except httpx.TimeoutException as e:
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.warning(
                "ai_gateway.timeout",
                endpoint=endpoint,
                latency_ms=latency_ms,
            )
            raise

    async def _get(self, endpoint: str) -> dict:
        """Make a GET request to the AI service."""
        client = await self._get_client()
        try:
            response = await client.get(endpoint)
            response.raise_for_status()
            return response.json()
        except Exception:
            raise

    async def health_check(self) -> dict:
        """Check if the AI service is healthy."""
        try:
            result = await self._get("/health")
            return {"status": "AVAILABLE", **result}
        except httpx.ConnectError:
            return {"status": "OFFLINE", "error": "Connection refused"}
        except httpx.TimeoutException:
            return {"status": "DEGRADED", "error": "Health check timeout"}
        except Exception as e:
            return {"status": "OFFLINE", "error": str(e)}

    async def close(self) -> None:
        """Close the HTTP client connection."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
