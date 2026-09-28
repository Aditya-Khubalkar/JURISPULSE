"""
JurisPulse — Standardised API Response Helpers
================================================
All API responses use a consistent envelope:

Success:
    {
        "success": true,
        "data": { ... },
        "message": "...",
        "meta": { "page": 1, "total": 100 }  # optional
    }

Error:
    {
        "success": false,
        "error": {
            "code": "RESOURCE_NOT_FOUND",
            "message": "Case not found.",
            "details": {}
        }
    }

Use the helpers below — never hand-craft response dicts in route handlers.
"""

from typing import Any, Optional

from fastapi import status
from fastapi.responses import JSONResponse


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = status.HTTP_200_OK,
    meta: Optional[dict] = None,
) -> JSONResponse:
    """Return a standardised success response."""
    body: dict[str, Any] = {
        "success": True,
        "message": message,
        "data": data,
    }
    if meta is not None:
        body["meta"] = meta
    return JSONResponse(content=body, status_code=status_code)


def created_response(
    data: Any = None,
    message: str = "Created successfully.",
) -> JSONResponse:
    """Return a 201 Created response."""
    return success_response(
        data=data,
        message=message,
        status_code=status.HTTP_201_CREATED,
    )


def no_content_response() -> JSONResponse:
    """Return a 204 No Content response."""
    return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)


def error_response(
    message: str,
    code: str = "ERROR",
    details: Optional[dict] = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> JSONResponse:
    """Return a standardised error response. Never include stack traces."""
    body: dict[str, Any] = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        },
    }
    return JSONResponse(content=body, status_code=status_code)


def paginated_response(
    data: list,
    total: int,
    page: int,
    page_size: int,
    message: str = "Success",
) -> JSONResponse:
    """Return a paginated response with metadata."""
    import math

    total_pages = math.ceil(total / page_size) if page_size > 0 else 1
    meta = {
        "page": page,
        "page_size": page_size,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
    return success_response(data=data, message=message, meta=meta)
