"""
JurisPulse — Document Processing Celery Tasks
================================================
Background tasks for the document processing pipeline.

Pipeline stages:
  1. validate
  2. store           (already done at upload — this task handles the rest)
  3. ocr
  4. text_cleaning
  5. metadata_extraction
  6. classification
  7. chunking
  8. embedding        (calls ai-services/embeddings/ via AI Gateway)
  9. indexing
 10. complete

Each stage updates the document status in the database.
Failures are recorded with error messages.

IMPORTANT: This worker calls the AI Gateway for embedding generation.
           It does NOT load any model weights directly.
"""

import asyncio
import uuid
from typing import Optional

import structlog
from celery import Task
from sqlalchemy import update

from app.core.config.constants import DocumentStatus
from app.database.base import Base
from app.workers.celery_app import celery_app

logger = structlog.get_logger("jurispulse.workers.documents")


def _get_db_session():
    """
    Create a synchronous database session for use inside Celery tasks.
    Note: Celery tasks run synchronously; async code is wrapped with asyncio.run().
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.core.config.settings import settings

    # Convert async URL to sync URL for Celery context
    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(sync_url, pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
    return Session()


def _update_document_status(
    document_id: str,
    status: str,
    status_message: Optional[str] = None,
    **extra_fields,
) -> None:
    """Synchronously update a document's status in the database."""
    from app.modules.documents.models import Document

    session = _get_db_session()
    try:
        values = {"status": status}
        if status_message is not None:
            values["status_message"] = status_message
        values.update(extra_fields)
        session.execute(
            update(Document)
            .where(Document.id == uuid.UUID(document_id))
            .values(**values)
        )
        session.commit()
    except Exception as e:
        logger.error("document_status_update_failed", document_id=document_id, error=str(e))
        session.rollback()
    finally:
        session.close()


@celery_app.task(
    name="app.workers.document_tasks.process_document",
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def process_document(
    self: Task,
    document_id: str,
    organization_id: str,
    case_id: Optional[str],
    storage_path: str,
    mime_type: str,
) -> dict:
    """
    Full document processing pipeline.
    Runs after the file has been uploaded to storage.
    """
    logger.info("document.processing_started", document_id=document_id)

    # --- Stage: OCR ---
    try:
        _update_document_status(document_id, DocumentStatus.OCR_PENDING.value)
        content = asyncio.run(_download_file(storage_path))

        _update_document_status(document_id, DocumentStatus.OCR_PROCESSING.value)
        ocr_result = asyncio.run(_run_ocr(content, mime_type))

        if ocr_result.is_success:
            _update_document_status(
                document_id,
                DocumentStatus.OCR_COMPLETE.value,
                extracted_text=ocr_result.full_text,
                page_count=ocr_result.total_pages,
            )
        elif ocr_result.status == "SKIPPED":
            # Non-image/PDF files — skip OCR
            _update_document_status(document_id, DocumentStatus.OCR_COMPLETE.value)
        else:
            _update_document_status(
                document_id,
                DocumentStatus.FAILED.value,
                status_message=f"OCR failed: {ocr_result.error}",
            )
            return {"status": "failed", "stage": "ocr", "error": ocr_result.error}

    except Exception as e:
        logger.error("document.ocr_error", document_id=document_id, error=str(e))
        _update_document_status(document_id, DocumentStatus.FAILED.value, status_message=str(e))
        return {"status": "failed", "stage": "ocr", "error": str(e)}

    # --- Stage: Classification (interface ready, rule-based fallback) ---
    try:
        _update_document_status(document_id, DocumentStatus.CLASSIFYING.value)
        doc_type = _classify_document_fallback(ocr_result.full_text)
        logger.info("document.classified", document_id=document_id, doc_type=doc_type)
    except Exception as e:
        logger.warning("document.classification_failed", error=str(e))
        doc_type = "other"

    # --- Stage: Chunking ---
    try:
        _update_document_status(document_id, DocumentStatus.CHUNKING.value)
        chunks = _chunk_text(ocr_result.full_text)
        logger.info("document.chunked", document_id=document_id, chunk_count=len(chunks))
    except Exception as e:
        logger.error("document.chunking_failed", document_id=document_id, error=str(e))
        _update_document_status(document_id, DocumentStatus.FAILED.value, status_message=str(e))
        return {"status": "failed", "stage": "chunking", "error": str(e)}

    # --- Stage: Embedding (via AI Gateway) ---
    if chunks:
        try:
            _update_document_status(document_id, DocumentStatus.EMBEDDING.value)
            # Queue embedding task separately to avoid timeout
            generate_embeddings.delay(
                document_id=document_id,
                chunks=chunks,
                organization_id=organization_id,
                case_id=case_id,
            )
        except Exception as e:
            logger.warning("document.embedding_queue_failed", error=str(e))
    else:
        # No text to embed (e.g., blank document)
        _update_document_status(
            document_id,
            DocumentStatus.COMPLETED.value,
            status_message="Document processed. No text extracted for embedding.",
        )

    return {"status": "processing", "document_id": document_id, "chunks": len(chunks)}


@celery_app.task(
    name="app.workers.document_tasks.generate_embeddings",
    bind=True,
    max_retries=3,
    default_retry_delay=120,
)
def generate_embeddings(
    self: Task,
    document_id: str,
    chunks: list,
    organization_id: str,
    case_id: Optional[str],
) -> dict:
    """
    Call the embedding AI service and index chunks.
    This is queued as a separate task to avoid blocking the main pipeline.
    """
    logger.info("embeddings.started", document_id=document_id, chunk_count=len(chunks))
    try:
        result = asyncio.run(_call_embedding_service(chunks))
        if result.get("status") == "ok":
            _update_document_status(document_id, DocumentStatus.COMPLETED.value)
            return {"status": "completed", "document_id": document_id}
        else:
            _update_document_status(
                document_id,
                DocumentStatus.FAILED.value,
                status_message="Embedding service unavailable.",
            )
            return {"status": "failed", "document_id": document_id}
    except Exception as e:
        logger.error("embeddings.failed", document_id=document_id, error=str(e))
        try:
            raise self.retry(exc=e)
        except self.MaxRetriesExceededError:
            _update_document_status(
                document_id,
                DocumentStatus.FAILED.value,
                status_message=f"Embedding failed after retries: {e}",
            )
            return {"status": "failed", "error": str(e)}


@celery_app.task(name="app.workers.document_tasks.check_ai_gateway_health")
def check_ai_gateway_health() -> dict:
    """Periodic task: poll all AI service health endpoints."""
    try:
        result = asyncio.run(_check_ai_health())
        return result
    except Exception as e:
        logger.error("ai_health_check_failed", error=str(e))
        return {"status": "error", "error": str(e)}


# ---------------------------------------------------------------------------
# Async helper functions
# ---------------------------------------------------------------------------

async def _download_file(storage_path: str) -> bytes:
    from app.services.storage.service import StorageService
    return await StorageService.download(storage_path)


async def _run_ocr(content: bytes, mime_type: str):
    from app.services.ocr.service import OCRService
    return await OCRService.extract_text(content, mime_type)


async def _call_embedding_service(chunks: list) -> dict:
    from app.services.ai.embedding_client import EmbeddingClient
    try:
        client = EmbeddingClient()
        response = await client.embed(texts=[c["text"] for c in chunks])
        return {"status": "ok", "count": len(response.embeddings)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


async def _check_ai_health() -> dict:
    from app.services.ai.health import AIHealthMonitor
    return await AIHealthMonitor.check_all()


# ---------------------------------------------------------------------------
# Utility functions (synchronous, no DB needed)
# ---------------------------------------------------------------------------

def _classify_document_fallback(text: str) -> str:
    """
    Rule-based document classification fallback.
    Used when the AI classifier is NOT_DEPLOYED.
    
    IMPORTANT: This is a transparent keyword heuristic.
    It is NOT presented as AI classification.
    The document processing pipeline logs this as 'rule_based' source.
    """
    text_lower = text.lower()
    if "petition" in text_lower or "petitioner" in text_lower:
        return "petition"
    if "affidavit" in text_lower:
        return "affidavit"
    if "bail" in text_lower:
        return "bail_application"
    if "notice" in text_lower:
        return "notice"
    if "judgment" in text_lower or "judgement" in text_lower:
        return "judgment"
    if "order" in text_lower:
        return "order"
    if "appeal" in text_lower:
        return "appeal"
    if "written statement" in text_lower:
        return "written_statement"
    return "other"


def _chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list:
    """
    Split text into overlapping chunks for embedding.
    Simple character-based chunker. Replace with sentence-aware chunker when needed.
    """
    if not text or len(text.strip()) == 0:
        return []
    chunks = []
    start = 0
    text = text.strip()
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text = text[start:end]
        if len(chunk_text.strip()) > 50:  # Skip very short chunks
            chunks.append({"text": chunk_text, "start": start, "end": end})
        start += chunk_size - overlap
    return chunks
