"""
JurisPulse — File Validation Utilities
========================================
Validates uploaded files for size, MIME type, extension, and basic content
integrity before they are accepted into the storage pipeline.

IMPORTANT: This module uses python-magic (libmagic) for MIME detection,
which checks actual file content — not the user-supplied filename.
Never trust the client-provided Content-Type header for security decisions.
"""

import hashlib
import os
from typing import Optional

import magic  # python-magic
from fastapi import UploadFile

from app.core.config.constants import (
    ALLOWED_EXTENSIONS,
    ALLOWED_MIME_TYPES,
    MAX_FILE_SIZE_BYTES,
)
from app.core.config.settings import settings
from app.utils.exceptions import (
    FileTooLargeError,
    FileValidationError,
    UnsupportedFileTypeError,
)


async def validate_and_read_upload(upload: UploadFile) -> tuple[bytes, str, str]:
    """
    Read the uploaded file into memory, validate it, and return:
        (file_bytes, detected_mime_type, sha256_checksum)

    Raises:
        FileTooLargeError: If file exceeds the configured size limit.
        UnsupportedFileTypeError: If MIME type or extension is not allowed.
        FileValidationError: For other validation failures.
    """
    content = await upload.read()
    if not content:
        raise FileValidationError("Uploaded file is empty.")

    # --- Size check ---
    if len(content) > settings.MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError(settings.MAX_FILE_SIZE_MB)

    # --- Extension check ---
    filename = upload.filename or "unknown"
    _, ext = os.path.splitext(filename.lower())
    if ext not in ALLOWED_EXTENSIONS:
        raise UnsupportedFileTypeError(ext)

    # --- MIME type detection (content-based) ---
    detected_mime = magic.from_buffer(content, mime=True)
    if detected_mime not in ALLOWED_MIME_TYPES:
        raise UnsupportedFileTypeError(detected_mime)

    # --- Checksum ---
    checksum = compute_checksum(content)

    return content, detected_mime, checksum


def compute_checksum(content: bytes, algorithm: str = "sha256") -> str:
    """Compute a hex digest checksum of file content."""
    h = hashlib.new(algorithm)
    h.update(content)
    return h.hexdigest()


def sanitize_filename(filename: Optional[str]) -> str:
    """
    Return a safe filename string.
    Strips path traversal characters and limits length.
    This is used only for display/metadata — never as a storage path.
    """
    if not filename:
        return "untitled"
    # Remove directory components
    name = os.path.basename(filename)
    # Replace problematic characters
    name = "".join(c if c.isalnum() or c in ("-", "_", ".") else "_" for c in name)
    # Limit length
    return name[:255]
