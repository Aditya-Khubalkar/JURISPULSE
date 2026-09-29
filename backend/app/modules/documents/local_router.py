"""
JurisPulse — Local Dev Upload Router
========================================
A lightweight upload endpoint that requires NO database or Supabase.
Files are saved to the local filesystem and metadata stored in a JSON file.

Available at: POST /api/v1/local/upload
             GET  /api/v1/local/documents
             GET  /api/v1/local/file/{file_id}
             DELETE /api/v1/local/documents/{file_id}

Only mounted when ENVIRONMENT=development.
"""

import json
import mimetypes
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.core.config.settings import settings

local_router = APIRouter()

# ── Storage paths ─────────────────────────────────────────────────────────────
STORAGE_ROOT = Path(settings.LOCAL_STORAGE_PATH) / "uploads"
METADATA_FILE = Path(settings.LOCAL_STORAGE_PATH) / "documents.json"

STORAGE_ROOT.mkdir(parents=True, exist_ok=True)

ALLOWED_MIMES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "image/png",
    "image/jpeg",
    "image/tiff",
}
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt", ".png", ".jpg", ".jpeg", ".tiff"}


# ── Metadata helpers ──────────────────────────────────────────────────────────

def _load_metadata() -> list[dict]:
    if METADATA_FILE.exists():
        try:
            return json.loads(METADATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save_metadata(docs: list[dict]) -> None:
    METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    METADATA_FILE.write_text(json.dumps(docs, indent=2, ensure_ascii=False), encoding="utf-8")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@local_router.post("/upload", summary="[Dev] Upload a document locally")
async def local_upload(
    file: UploadFile = File(...),
    case_id: Optional[str] = Form(default=None),
    name: Optional[str] = Form(default=None),
):
    """
    Upload a document to local disk (no DB, no Supabase, no auth required).
    Available in development mode only.
    """
    # Detect MIME
    suffix = Path(file.filename or "file").suffix.lower()
    detected_mime = file.content_type or mimetypes.guess_type(file.filename or "")[0] or "application/octet-stream"

    # Validate extension
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{suffix}' is not allowed. Accepted: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    # Read content
    content = await file.read()
    size_bytes = len(content)

    # Check size
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if size_bytes > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds the {settings.MAX_FILE_SIZE_MB} MB limit.",
        )

    # Save to disk
    file_id = str(uuid.uuid4())
    safe_name = f"{file_id}{suffix}"
    disk_path = STORAGE_ROOT / safe_name
    disk_path.write_bytes(content)

    # Build metadata entry
    display_name = name or Path(file.filename or "document").stem.replace("_", " ").replace("-", " ")
    doc = {
        "id": file_id,
        "name": display_name,
        "original_filename": file.filename,
        "mime_type": detected_mime,
        "size_bytes": size_bytes,
        "file_path": str(disk_path),
        "suffix": suffix,
        "case_id": case_id,
        "status": "stored",
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }

    # Persist metadata
    docs = _load_metadata()
    docs.insert(0, doc)
    _save_metadata(docs)

    return {
        "success": True,
        "data": {
            "document_id": file_id,
            "name": display_name,
            "original_filename": file.filename,
            "mime_type": detected_mime,
            "size_bytes": size_bytes,
            "status": "stored",
            "uploaded_at": doc["uploaded_at"],
            "download_url": f"/api/v1/local/file/{file_id}",
        },
        "message": "Document uploaded successfully.",
    }


@local_router.get("/documents", summary="[Dev] List locally stored documents")
async def local_list_documents(
    search: Optional[str] = None,
    case_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
):
    """List all locally uploaded documents."""
    docs = _load_metadata()

    if search:
        q = search.lower()
        docs = [d for d in docs if q in (d.get("name") or "").lower() or q in (d.get("original_filename") or "").lower()]
    if case_id:
        docs = [d for d in docs if d.get("case_id") == case_id]

    total = len(docs)
    page = docs[offset: offset + limit]

    # Add download_url to each
    for d in page:
        d["download_url"] = f"/api/v1/local/file/{d['id']}"

    return {
        "success": True,
        "data": page,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@local_router.get("/file/{file_id}", summary="[Dev] Download a local file")
async def local_download_file(file_id: str):
    """Serve a locally stored file."""
    docs = _load_metadata()
    doc = next((d for d in docs if d["id"] == file_id), None)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    disk_path = Path(doc["file_path"])
    if not disk_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk.")

    return FileResponse(
        path=str(disk_path),
        media_type=doc.get("mime_type", "application/octet-stream"),
        filename=doc.get("original_filename", disk_path.name),
    )


@local_router.delete("/documents/{file_id}", summary="[Dev] Delete a local document")
async def local_delete_document(file_id: str):
    """Delete a locally stored document."""
    docs = _load_metadata()
    doc = next((d for d in docs if d["id"] == file_id), None)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    # Delete file from disk
    disk_path = Path(doc["file_path"])
    if disk_path.exists():
        disk_path.unlink()

    # Remove from metadata
    docs = [d for d in docs if d["id"] != file_id]
    _save_metadata(docs)

    return {"success": True, "message": "Document deleted."}
