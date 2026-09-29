"""
JurisPulse — Request ID Middleware
=====================================
Attaches a unique X-Request-ID header to every request and response.
The ID is injected into structlog context so all log lines for a
given request carry the same ID, enabling end-to-end request tracing.
"""

import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

REQUEST_ID_HEADER = "X-Request-ID"


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that:
    1. Reads the incoming X-Request-ID header (if present).
    2. Generates a new UUID if no header is provided.
    3. Binds the ID to the structlog context variable store.
    4. Adds X-Request-ID to the outgoing response headers.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())

        # Store in request state so other middleware/handlers can read it
        request.state.request_id = request_id

        # Bind to structlog context (cleared automatically per async context)
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response
