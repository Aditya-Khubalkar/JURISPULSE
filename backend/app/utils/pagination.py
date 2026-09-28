"""
JurisPulse — Pagination Utilities
===================================
Standardised query parameter handling and pagination metadata.
"""

from typing import Optional
from fastapi import Query
from pydantic import BaseModel, Field

from app.core.config.settings import settings
from app.core.config.constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


class PaginationParams(BaseModel):
    """Pagination parameters parsed from query string."""

    page: int = Field(default=DEFAULT_PAGE, ge=1)
    page_size: int = Field(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


def get_pagination_params(
    page: int = Query(default=DEFAULT_PAGE, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(
        default=DEFAULT_PAGE_SIZE,
        ge=1,
        le=MAX_PAGE_SIZE,
        alias="page_size",
        description="Number of items per page",
    ),
) -> PaginationParams:
    """FastAPI dependency that extracts and validates pagination query params."""
    return PaginationParams(page=page, page_size=page_size)


class PaginationMeta(BaseModel):
    """Metadata included in paginated list responses."""

    page: int
    page_size: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool


def build_pagination_meta(
    total: int,
    page: int,
    page_size: int,
) -> PaginationMeta:
    """Compute pagination metadata from total count and current page."""
    import math

    total_pages = math.ceil(total / page_size) if page_size > 0 else 1
    return PaginationMeta(
        page=page,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1,
    )
