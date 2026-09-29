"""
JurisPulse — AI Gateway: Health Monitor
==========================================
Polls all registered AI services and updates their status in the registry.
Called at startup and periodically via a Celery beat task.
"""

import asyncio
import time
from datetime import datetime, timezone
from typing import Dict

import structlog

from app.services.ai.registry import AIModelRegistryService
from app.core.config.constants import ModelStatus

logger = structlog.get_logger("jurispulse.ai_gateway.health")


class AIHealthMonitor:
    """Polls AI service health endpoints and updates the registry."""

    @classmethod
    async def initialize(cls) -> None:
        """
        Called at application startup.
        Initialises the registry and runs an initial health check.
        """
        AIModelRegistryService.initialize()
        await cls.check_all()

    @classmethod
    async def check_all(cls) -> Dict[str, str]:
        """
        Poll all enabled AI services concurrently.
        Returns a dict of {model_id: status_string}.
        """
        import httpx

        models = AIModelRegistryService.get_all()
        enabled = [m for m in models if m.is_enabled and m.endpoint]

        results: Dict[str, str] = {}

        async def _check_one(model_id: str, endpoint: str) -> None:
            start = time.perf_counter()
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(f"{endpoint}/health")
                    latency_ms = round((time.perf_counter() - start) * 1000, 2)
                    if response.status_code == 200:
                        AIModelRegistryService.update_status(
                            model_id, ModelStatus.AVAILABLE, latency_ms
                        )
                        results[model_id] = "AVAILABLE"
                    else:
                        AIModelRegistryService.update_status(
                            model_id, ModelStatus.DEGRADED, latency_ms
                        )
                        results[model_id] = "DEGRADED"
            except Exception as e:
                AIModelRegistryService.update_status(model_id, ModelStatus.OFFLINE)
                results[model_id] = "OFFLINE"
                logger.debug("health_monitor.offline", model_id=model_id, error=str(e))

        if enabled:
            await asyncio.gather(*[_check_one(m.model_id, m.endpoint) for m in enabled])

        # NOT_DEPLOYED models stay NOT_DEPLOYED — never mark as AVAILABLE
        not_deployed = [m for m in models if not m.is_enabled]
        for m in not_deployed:
            results[m.model_id] = "NOT_DEPLOYED"

        logger.info("health_monitor.checked", results=results)
        return results

    @classmethod
    def get_health_summary(cls) -> Dict:
        """Return a serialisable health summary for the admin API."""
        models = AIModelRegistryService.get_all()
        return {
            m.model_id: {
                "name": m.name,
                "status": m.status.value if hasattr(m.status, "value") else m.status,
                "is_enabled": m.is_enabled,
                "last_check": m.last_health_check.isoformat() if m.last_health_check else None,
                "latency_ms": m.last_latency_ms,
            }
            for m in models
        }
