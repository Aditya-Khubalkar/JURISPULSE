"""
JurisPulse — Structured Logging Configuration
================================================
Sets up Python logging with structlog for structured JSON output.
Request IDs are automatically injected via context variables.
Sensitive fields are redacted before logging.
"""

import logging
import logging.config
import sys
from typing import Any, Dict

import structlog
from structlog.types import EventDict, WrappedLogger

from app.core.config.settings import settings


# ---------------------------------------------------------------------------
# Sensitive field redaction processor
# ---------------------------------------------------------------------------

_SENSITIVE_KEYS = frozenset(settings.LOG_SENSITIVE_FIELDS)


def _redact_sensitive(
    logger: WrappedLogger,
    method_name: str,
    event_dict: EventDict,
) -> EventDict:
    """Recursively redact sensitive keys from log event dicts."""
    for key in list(event_dict.keys()):
        if key.lower() in _SENSITIVE_KEYS:
            event_dict[key] = "***REDACTED***"
        elif isinstance(event_dict[key], dict):
            event_dict[key] = _redact_nested(event_dict[key])
    return event_dict


def _redact_nested(data: Dict[str, Any]) -> Dict[str, Any]:
    result = {}
    for k, v in data.items():
        if k.lower() in _SENSITIVE_KEYS:
            result[k] = "***REDACTED***"
        elif isinstance(v, dict):
            result[k] = _redact_nested(v)
        else:
            result[k] = v
    return result


# ---------------------------------------------------------------------------
# Shared processors (both dev and prod)
# ---------------------------------------------------------------------------

_SHARED_PROCESSORS = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(fmt="iso", utc=True),
    structlog.processors.StackInfoRenderer(),
    _redact_sensitive,
]


def configure_logging() -> None:
    """
    Configure structlog + stdlib logging.
    Call once at application startup (in main.py lifespan).
    """
    log_level_name = settings.LOG_LEVEL.upper()
    log_level = getattr(logging, log_level_name, logging.INFO)

    use_json = settings.LOG_FORMAT.lower() == "json"

    if use_json:
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            *_SHARED_PROCESSORS,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=_SHARED_PROCESSORS,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(log_level)

    # Quieten noisy libraries
    for noisy_lib in ["uvicorn.access", "sqlalchemy.engine", "httpx", "httpcore"]:
        lib_logger = logging.getLogger(noisy_lib)
        lib_logger.setLevel(logging.WARNING)

    # uvicorn uses its own logging - keep it consistent
    logging.getLogger("uvicorn").setLevel(log_level)
    logging.getLogger("uvicorn.error").setLevel(log_level)
    logging.getLogger("celery").setLevel(log_level)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Return a structured logger with the given name."""
    return structlog.get_logger(name)
