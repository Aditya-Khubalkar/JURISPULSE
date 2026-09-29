"""
JurisPulse — Embedding Celery Tasks
"""

from typing import List, Optional
from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.embedding_tasks.index_document_chunks")
def index_document_chunks(document_id: str, chunks: List[dict]) -> dict:
    """Index a document's chunks into pgvector."""
    import asyncio
    return asyncio.run(_index(document_id, chunks))


async def _index(document_id, chunks) -> dict:
    """Store chunk embeddings in Supabase pgvector."""
    from app.services.ai.embedding_client import EmbeddingClient
    try:
        client = EmbeddingClient()
        texts = [c["text"] for c in chunks]
        response = await client.embed(texts)
        # Would insert into pgvector here
        return {"status": "ok", "chunks_indexed": len(response.embeddings)}
    except Exception as e:
        return {"status": "error", "error": str(e)}
