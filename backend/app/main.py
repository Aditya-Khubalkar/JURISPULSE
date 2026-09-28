"""
JurisPulse — FastAPI Application Factory
==========================================
This is the entry point for the backend.

Architecture enforced here:
  - CORS (configured from settings — not hard-coded)
  - Middleware stack (order matters: outer → inner)
  - Exception handlers (no stack trace leakage)
  - API router (all routes live in api/router.py)
  - Lifespan context (startup / shutdown hooks)

The application NEVER:
  - Loads model weights
  - Imports PyTorch / transformers / Unsloth
  - Communicates directly with model URLs (that is the AI Gateway's job)
"""

import sys
import asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import structlog
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError as PydanticValidationError

from app.core.config.logging import configure_logging, get_logger
from app.core.config.settings import settings
from app.middleware.logging import HTTPLoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.security import SecurityHeadersMiddleware
from app.utils.exceptions import JurisPulseError

logger = get_logger("jurispulse.app")


# ---------------------------------------------------------------------------
# Lifespan — startup and shutdown
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.
    Runs on startup and teardown.
    """
    # --- Startup ---
    configure_logging()
    logger.info(
        "jurispulse.startup",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )

    # Initialise AI Gateway model registry health checks
    try:
        from app.services.ai.health import AIHealthMonitor
        await AIHealthMonitor.initialize()
    except Exception as e:
        logger.warning("ai_gateway.init_failed", error=str(e))

    yield

    # --- Shutdown ---
    logger.info("jurispulse.shutdown")

    try:
        from app.database.session import engine
        await engine.dispose()
    except Exception as e:
        logger.error("database.dispose_failed", error=str(e))


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title="JurisPulse API",
        description=(
            "Multi-agent legal workflow orchestration platform for Indian legal professionals. "
            "Provides case management, document processing, legal research, AI-assisted drafting, "
            "and hallucination detection for legal documents."
        ),
        version=settings.APP_VERSION,
        docs_url="/api/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/api/redoc" if settings.ENVIRONMENT != "production" else None,
        openapi_url="/api/openapi.json" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
    )

    # ---- Middleware (outermost → innermost) ----
    # NOTE: The order here matters.
    # Requests travel top → bottom through the middleware stack.
    # Responses travel bottom → top.

    # CORS — must be first so preflight OPTIONS requests are handled correctly
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOWED_METHODS,
        allow_headers=settings.CORS_ALLOWED_HEADERS,
    )

    # Security headers — attach before logging so they're visible in access logs
    app.add_middleware(SecurityHeadersMiddleware)

    # Rate limiting — checked before processing begins
    app.add_middleware(RateLimitMiddleware)

    # Request ID — must come before logging so the ID is available in log lines
    app.add_middleware(RequestIDMiddleware)

    # HTTP logging — innermost middleware, has access to request state
    app.add_middleware(HTTPLoggingMiddleware)

    # ---- Exception Handlers ----
    _register_exception_handlers(app)

    # ---- Routers ----
    from app.api.router import api_router
    app.include_router(api_router)

    return app


def _register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers.
    No stack traces are ever exposed to clients.
    Request IDs are included in error responses for support tracing.
    """

    @app.exception_handler(JurisPulseError)
    async def jurispulse_exception_handler(
        request: Request, exc: JurisPulseError
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        logger.warning(
            "jurispulse.handled_exception",
            error_code=exc.error_code,
            message=exc.message,
            path=request.url.path,
            request_id=request_id,
        )
        body = {
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            },
        }
        if request_id:
            body["request_id"] = request_id
        return JSONResponse(status_code=exc.http_status_code, content=body)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        # Extract human-readable field errors
        errors = []
        for error in exc.errors():
            loc = " → ".join(str(x) for x in error["loc"] if x != "body")
            errors.append({"field": loc, "message": error["msg"]})

        logger.info(
            "jurispulse.validation_error",
            errors=errors,
            path=request.url.path,
            request_id=request_id,
        )
        body = {
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed.",
                "details": {"errors": errors},
            },
        }
        if request_id:
            body["request_id"] = request_id
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=body,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", None)
        logger.exception(
            "jurispulse.unhandled_exception",
            path=request.url.path,
            request_id=request_id,
        )
        body = {
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected internal error occurred. Please try again.",
                "details": {},
            },
        }
        if request_id:
            body["request_id"] = request_id
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=body,
        )


# ---------------------------------------------------------------------------
# WSGI/ASGI entry point
# ---------------------------------------------------------------------------

app: FastAPI = create_application()
