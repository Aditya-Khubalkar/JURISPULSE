"""
JurisPulse — Retrieval: Vector Search
========================================
Queries the existing Supabase pgvector index for semantically similar
legal chunks.

CRITICAL:
  - The existing ~14,544 indexed chunks are NOT migrated or recreated.
  - The dynamic count is fetched from the database — never hard-coded.
  - Query embedding is obtained from the AI Gateway (bge-small service).
  - Results carry full provenance (chunk_id, document_id, source, score).

Vector search uses Supabase's pgvector via the RPC function
VECTOR_SEARCH_FUNCTION (default: match_legal_chunks).

The match_legal_chunks function signature expected in Supabase:
  CREATE OR REPLACE FUNCTION match_legal_chunks(
    query_embedding vector(384),
    match_count int DEFAULT 10,
    filter jsonb DEFAULT '{}'
  )
  RETURNS TABLE (
    id uuid, chunk_id text, document_id text, source_id text,
    text text, metadata jsonb, similarity float
  )
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import structlog

from app.core.config.settings import settings

logger = structlog.get_logger("jurispulse.retrieval.vector_search")


@dataclass
class RetrievedChunk:
    """A retrieved legal chunk with full provenance."""

    chunk_id: str
    document_id: Optional[str]
    source_id: Optional[str]
    text: str
    metadata: Dict[str, Any]
    similarity_score: float

    @property
    def is_relevant(self) -> bool:
        """Consider chunks with similarity > 0.7 as relevant."""
        return self.similarity_score >= 0.70


class VectorSearch:
    """
    Queries the Supabase pgvector index for the existing legal corpus.
    Never recreates or migrates the existing index.
    """

    def __init__(self) -> None:
        from supabase import create_client
        self._supabase = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY,
        )

    async def search(
        self,
        query_embedding: List[float],
        limit: int = settings.DEFAULT_SEARCH_LIMIT,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievedChunk]:
        """
        Run vector similarity search against the existing legal corpus.

        Args:
            query_embedding: Dense vector from bge-small (384 dimensions)
            limit: Max results to return
            metadata_filter: Optional pgvector filter (e.g., {"court": "Supreme Court"})

        Returns:
            List of RetrievedChunk ordered by similarity (highest first)
        """
        try:
            params = {
                "query_embedding": query_embedding,
                "match_count": min(limit, settings.MAX_SEARCH_LIMIT),
            }
            if metadata_filter:
                params["filter"] = metadata_filter

            response = self._supabase.rpc(
                settings.VECTOR_SEARCH_FUNCTION,
                params,
            ).execute()

            if not response.data:
                return []

            chunks = []
            for row in response.data:
                chunks.append(RetrievedChunk(
                    chunk_id=str(row.get("id", "") or row.get("chunk_id", "")),
                    document_id=row.get("document_id"),
                    source_id=row.get("source_id"),
                    text=row.get("text", ""),
                    metadata=row.get("metadata") or {},
                    similarity_score=float(row.get("similarity", 0.0)),
                ))
            return chunks

        except Exception as e:
            logger.error("vector_search.failed", error=str(e))
            return []

    async def get_corpus_stats(self) -> Dict[str, Any]:
        """
        Return dynamic corpus statistics.
        The chunk count is fetched from the database — NEVER hard-coded.
        """
        try:
            # Get total chunk count
            chunks_result = self._supabase.table(settings.VECTOR_SEARCH_TABLE).select(
                "id", count="exact"
            ).execute()
            total_chunks = chunks_result.count if hasattr(chunks_result, "count") else 0

            return {
                "total_chunks": total_chunks,
                "embedding_model": "bge-small-en-v1.5",
                "embedding_dimension": settings.EMBEDDING_DIMENSION,
                "index_table": settings.VECTOR_SEARCH_TABLE,
                "index_status": "READY" if total_chunks > 0 else "EMPTY",
            }
        except Exception as e:
            logger.error("corpus_stats.failed", error=str(e))
            return {
                "total_chunks": None,
                "index_status": "UNKNOWN",
                "error": str(e),
            }
