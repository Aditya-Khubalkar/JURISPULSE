"""
JurisPulse — Legal Research Service
=======================================
Orchestrates the full RAG retrieval pipeline:

  User Query
       ↓
  Query Validation
       ↓
  Query Embedding (bge-small via AI Gateway)
       ↓
  Vector Search (Supabase pgvector)
       ↓
  Metadata Filtering
       ↓
  Candidate Retrieval
       ↓
  Ranking
       ↓
  Evidence Selection
       ↓
  Source Attribution
       ↓
  Result

Every retrieved chunk maintains full provenance.
If the embedding service is unavailable, the service returns a clear error
rather than fabricating results.
"""

import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.ai.embedding_client import EmbeddingClient
from app.modules.research.models import ResearchQuery, ResearchResult
from app.modules.retrieval.vector_search import RetrievedChunk, VectorSearch
from app.utils.exceptions import EmbeddingServiceError, ModelUnavailableError

logger = structlog.get_logger("jurispulse.research.service")


class ResearchService:
    """
    Legal research service — RAG pipeline orchestrator.
    """

    @staticmethod
    async def search(
        db: AsyncSession,
        query_text: str,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        case_id: Optional[uuid.UUID] = None,
        limit: int = 10,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run a semantic legal research query.
        Returns results with full provenance or a clear error if unavailable.
        """
        start_time = time.perf_counter()

        # Create query record
        query_record = ResearchQuery(
            organization_id=organization_id,
            case_id=case_id,
            user_id=user_id,
            query_text=query_text,
            status="PROCESSING",
        )
        db.add(query_record)
        await db.flush()

        # --- Step 1: Embed the query ---
        try:
            embedding_client = EmbeddingClient()
            query_embedding = await embedding_client.embed_query(query_text)
        except (ModelUnavailableError, EmbeddingServiceError) as e:
            query_record.status = "FAILED"
            query_record.error = str(e)
            await db.flush()
            return {
                "query_id": str(query_record.id),
                "query": query_text,
                "status": "FAILED",
                "error": str(e),
                "results": [],
                "message": "Embedding service is unavailable. Research cannot be performed.",
            }

        # --- Step 2: Vector search ---
        try:
            vector_search = VectorSearch()
            chunks = await vector_search.search(
                query_embedding=query_embedding,
                limit=limit,
                metadata_filter=metadata_filter,
            )
        except Exception as e:
            logger.error("research.vector_search_failed", error=str(e))
            query_record.status = "FAILED"
            query_record.error = str(e)
            await db.flush()
            return {
                "query_id": str(query_record.id),
                "status": "FAILED",
                "error": "Vector search failed.",
                "results": [],
            }

        # --- Step 3: Store results with provenance ---
        result_records = []
        for rank, chunk in enumerate(chunks, start=1):
            rr = ResearchResult(
                query_id=query_record.id,
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                source_id=chunk.source_id,
                text=chunk.text,
                similarity_score=chunk.similarity_score,
                rank=rank,
                metadata=chunk.metadata,
                created_at=datetime.now(timezone.utc),
            )
            db.add(rr)
            result_records.append(rr)
        await db.flush()

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        query_record.status = "COMPLETED"
        query_record.result_count = len(chunks)
        query_record.embedding_model = "bge-small-en-v1.5"
        query_record.latency_ms = elapsed_ms
        await db.flush()

        logger.info(
            "research.completed",
            query_id=str(query_record.id),
            result_count=len(chunks),
            latency_ms=elapsed_ms,
        )

        return {
            "query_id": str(query_record.id),
            "query": query_text,
            "status": "COMPLETED",
            "result_count": len(chunks),
            "latency_ms": elapsed_ms,
            "results": [
                {
                    "rank": rank,
                    "chunk_id": chunk.chunk_id,
                    "document_id": chunk.document_id,
                    "source_id": chunk.source_id,
                    "text": chunk.text,
                    "similarity_score": chunk.similarity_score,
                    "is_relevant": chunk.is_relevant,
                    "metadata": chunk.metadata,
                }
                for rank, chunk in enumerate(chunks, start=1)
            ],
        }

    @staticmethod
    async def get_corpus_stats() -> Dict[str, Any]:
        """Return dynamic corpus statistics. Count from DB, never hard-coded."""
        try:
            vector_search = VectorSearch()
            return await vector_search.get_corpus_stats()
        except Exception as e:
            return {"error": str(e), "index_status": "UNKNOWN"}
