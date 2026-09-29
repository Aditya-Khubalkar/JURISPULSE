"""
JurisPulse — Research Router
================================
Routes: /api/v1/research/*
"""

import uuid
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.database.session import get_db
from app.modules.research.service import ResearchService
from app.utils.responses import success_response

research_router = APIRouter()


class SearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=1000)
    case_id: Optional[uuid.UUID] = None
    limit: int = Field(default=10, ge=1, le=50)
    metadata_filter: Optional[Dict[str, Any]] = None


@research_router.post("/search", summary="Search legal corpus")
async def search(
    body: SearchRequest,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """
    Perform a semantic search over the indexed Indian legal corpus.
    
    Returns ranked results with full source provenance.
    If the embedding service is unavailable, returns a clear error.
    Results are never fabricated.
    """
    result = await ResearchService.search(
        db=db,
        query_text=body.query,
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        case_id=body.case_id,
        limit=body.limit,
        metadata_filter=body.metadata_filter,
    )
    return success_response(data=result)


@research_router.get("/stats", summary="Get corpus statistics")
async def get_corpus_stats(
    current_user: User = Depends(CurrentUser),
):
    """
    Return statistics about the indexed legal corpus.
    Chunk count is fetched from the database — never hard-coded.
    """
    stats = await ResearchService.get_corpus_stats()
    return success_response(data=stats)


@research_router.get("/{query_id}", summary="Get research query by ID")
async def get_query(
    query_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Get a previously executed research query and its results."""
    from sqlalchemy import select
    from app.modules.research.models import ResearchQuery, ResearchResult

    result = await db.execute(
        select(ResearchQuery).where(
            ResearchQuery.id == query_id,
            ResearchQuery.organization_id == current_user.organization_id,
        )
    )
    query = result.scalar_one_or_none()
    if not query:
        from app.utils.exceptions import NotFoundError
        raise NotFoundError("Research query", str(query_id))

    results = await db.execute(
        select(ResearchResult)
        .where(ResearchResult.query_id == query_id)
        .order_by(ResearchResult.rank)
    )
    chunks = results.scalars().all()

    return success_response(data={
        "query_id": str(query.id),
        "query": query.query_text,
        "status": query.status,
        "result_count": query.result_count,
        "embedding_model": query.embedding_model,
        "latency_ms": query.latency_ms,
        "created_at": query.created_at.isoformat(),
        "results": [
            {
                "rank": c.rank,
                "chunk_id": c.chunk_id,
                "document_id": c.document_id,
                "source_id": c.source_id,
                "text": c.text,
                "similarity_score": c.similarity_score,
                "metadata": c.metadata,
            }
            for c in chunks
        ],
    })
