"""
JurisPulse — Documents Router
================================
Routes: /api/v1/documents/*

Upload flow:
  POST /documents/upload
     → validate file (size, MIME, extension)
     → store in cloud storage
     → create Document record in DB
     → queue background processing task
     → return document ID
"""

import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.core.config.constants import DocumentStatus
from app.core.config.settings import settings
from app.database.session import get_db
from app.modules.documents.models import Document, DocumentVersion
from app.services.storage.service import StorageService
from app.utils.exceptions import CaseAccessDeniedError, NotFoundError
from app.utils.file_validation import sanitize_filename, validate_and_read_upload
from app.utils.responses import created_response, success_response
from sqlalchemy import select

documents_router = APIRouter()


@documents_router.post(
    "/upload",
    summary="Upload a document",
    status_code=201,
)
async def upload_document(
    file: UploadFile = File(...),
    case_id: Optional[uuid.UUID] = Form(default=None),
    name: Optional[str] = Form(default=None),
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a legal document.
    Accepted: PDF, JPEG, PNG, TIFF, DOC, DOCX, TXT (max 50 MB).
    The file is stored immediately; OCR and embedding run in the background.
    """
    # Validate case membership if case_id provided
    if case_id:
        from app.modules.cases.models import CaseMember
        member = await db.execute(
            select(CaseMember).where(
                CaseMember.case_id == case_id,
                CaseMember.user_id == current_user.id,
            )
        )
        if not member.scalar_one_or_none():
            raise CaseAccessDeniedError()

    # Validate and read the upload
    content, detected_mime, checksum = await validate_and_read_upload(file)
    safe_filename = sanitize_filename(file.filename)
    display_name = name or safe_filename

    # Upload to storage (path is UUID-based, never from user input)
    storage_path = await StorageService.upload_document(
        content=content,
        organization_id=str(current_user.organization_id),
        case_id=str(case_id) if case_id else None,
        original_filename=safe_filename,
        mime_type=detected_mime,
    )

    # Create Document record
    doc = Document(
        organization_id=current_user.organization_id,
        case_id=case_id,
        name=display_name,
        original_filename=safe_filename,
        mime_type=detected_mime,
        size_bytes=len(content),
        checksum=checksum,
        storage_path=storage_path,
        storage_provider=settings.STORAGE_PROVIDER,
        status=DocumentStatus.STORED.value,
        uploaded_by=current_user.id,
    )
    db.add(doc)
    await db.flush()
    await db.refresh(doc)

    # Create initial version record
    version = DocumentVersion(
        document_id=doc.id,
        version_number=1,
        storage_path=storage_path,
        checksum=checksum,
        size_bytes=len(content),
        created_by=current_user.id,
        created_at=datetime.now(timezone.utc),
    )
    db.add(version)
    await db.flush()

    # Queue background processing
    from app.workers.document_tasks import process_document
    process_document.delay(
        document_id=str(doc.id),
        organization_id=str(current_user.organization_id),
        case_id=str(case_id) if case_id else None,
        storage_path=storage_path,
        mime_type=detected_mime,
    )

    return created_response(
        data={
            "document_id": str(doc.id),
            "name": doc.name,
            "status": doc.status,
            "size_bytes": doc.size_bytes,
            "mime_type": doc.mime_type,
            "processing": "Document is being processed in the background.",
        },
        message="Document uploaded successfully.",
    )


@documents_router.get("/{document_id}", summary="Get document info")
async def get_document(
    document_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Get document metadata and processing status."""
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.organization_id == current_user.organization_id,
        )
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise NotFoundError("Document", str(document_id))

    return success_response(
        data={
            "id": str(doc.id),
            "name": doc.name,
            "original_filename": doc.original_filename,
            "mime_type": doc.mime_type,
            "size_bytes": doc.size_bytes,
            "status": doc.status,
            "status_message": doc.status_message,
            "page_count": doc.page_count,
            "document_type": doc.document_type,
            "case_id": str(doc.case_id) if doc.case_id else None,
            "uploaded_by": str(doc.uploaded_by),
            "created_at": doc.created_at.isoformat(),
        }
    )


@documents_router.get("/{document_id}/download-url", summary="Get presigned download URL")
async def get_document_download_url(
    document_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Get a presigned URL to download the document file (valid for 1 hour)."""
    result = await db.execute(
        select(Document).where(
            Document.id == document_id,
            Document.organization_id == current_user.organization_id,
        )
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise NotFoundError("Document", str(document_id))

    url = await StorageService.get_url(doc.storage_path, expires_in=3600)
    return success_response(data={"url": url, "expires_in": 3600})
