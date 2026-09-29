"""
JurisPulse — HTTP Request / Response Logging Middleware
==========================================================
Logs every incoming request and outgoing response at INFO level.
Sensitive headers are redacted before logging.
"""

import time

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = structlog.get_logger("jurispulse.http")

_SENSITIVE_HEADERS = frozenset(
    ["authorization", "cookie", "x-api-key", "x-auth-token"]
)

# Paths that are too noisy to log at INFO (health checks etc.)
_SKIP_PATHS = frozenset(["/api/v1/health", "/favicon.ico"])


def _sanitize_headers(headers: dict) -> dict:
    return {
        k: ("***" if k.lower() in _SENSITIVE_HEADERS else v)
        for k, v in headers.items()
    }


class HTTPLoggingMiddleware(BaseHTTPMiddleware):
    """Log each HTTP request/response pair with timing and status code."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        if request.url.path in _SKIP_PATHS:
            return await call_next(request)

        start_time = time.perf_counter()
        request_id = getattr(request.state, "request_id", None)

        logger.info(
            "http.request",
            method=request.method,
            path=request.url.path,
            query=str(request.url.query) or None,
            client=request.client.host if request.client else None,
            request_id=request_id,
        )

        try:
            response: Response = await call_next(request)
        except Exception as exc:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(
                "http.error",
                method=request.method,
                path=request.url.path,
                request_id=request_id,
                error=str(exc),
                elapsed_ms=elapsed_ms,
            )
            raise

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.info(
            "http.response",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            elapsed_ms=elapsed_ms,
            request_id=request_id,
        )
        return response
