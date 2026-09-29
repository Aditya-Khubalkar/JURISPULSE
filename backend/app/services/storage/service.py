"""
JurisPulse — Storage Abstraction
===================================
Abstract interface + provider implementations for file storage.
Business code only interacts with StorageService — never with provider SDKs directly.

Providers implemented:
  - SupabaseStorageProvider (default)
  - LocalStorageProvider (development / testing)

Future providers can be added without touching any business code:
  - MinIOStorageProvider
  - S3CompatibleStorageProvider
"""

import abc
import os
import uuid
from pathlib import Path
from typing import BinaryIO, Optional

import structlog

from app.core.config.settings import settings

logger = structlog.get_logger("jurispulse.storage")


# ---------------------------------------------------------------------------
# Abstract interface
# ---------------------------------------------------------------------------

class StorageProvider(abc.ABC):
    """Abstract storage provider. All providers must implement this interface."""

    @abc.abstractmethod
    async def upload(
        self,
        content: bytes,
        storage_path: str,
        mime_type: str,
    ) -> str:
        """Upload file content. Returns the storage path."""

    @abc.abstractmethod
    async def download(self, storage_path: str) -> bytes:
        """Download file content by storage path."""

    @abc.abstractmethod
    async def delete(self, storage_path: str) -> bool:
        """Delete a file. Returns True on success."""

    @abc.abstractmethod
    async def exists(self, storage_path: str) -> bool:
        """Check if a file exists at the given path."""

    @abc.abstractmethod
    async def get_url(self, storage_path: str, expires_in: int = 3600) -> str:
        """Return a presigned or public URL for the file."""


# ---------------------------------------------------------------------------
# Supabase Storage Provider
# ---------------------------------------------------------------------------

class SupabaseStorageProvider(StorageProvider):
    """
    Stores files in Supabase Storage.
    Uses the service role key for all operations.
    """

    def __init__(self) -> None:
        from supabase import create_client
        self._client = create_client(
            settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY
        )
        self._bucket = settings.STORAGE_BUCKET

    async def upload(self, content: bytes, storage_path: str, mime_type: str) -> str:
        try:
            self._client.storage.from_(self._bucket).upload(
                path=storage_path,
                file=content,
                file_options={"content-type": mime_type, "upsert": "false"},
            )
            logger.info("storage.uploaded", path=storage_path, size=len(content))
            return storage_path
        except Exception as e:
            logger.error("storage.upload_failed", path=storage_path, error=str(e))
            from app.utils.exceptions import StorageError
            raise StorageError(f"Failed to upload file: {e}")

    async def download(self, storage_path: str) -> bytes:
        try:
            response = self._client.storage.from_(self._bucket).download(storage_path)
            return response
        except Exception as e:
            from app.utils.exceptions import StorageError
            raise StorageError(f"Failed to download file: {e}")

    async def delete(self, storage_path: str) -> bool:
        try:
            self._client.storage.from_(self._bucket).remove([storage_path])
            return True
        except Exception as e:
            logger.error("storage.delete_failed", path=storage_path, error=str(e))
            return False

    async def exists(self, storage_path: str) -> bool:
        try:
            self._client.storage.from_(self._bucket).list(path=storage_path)
            return True
        except Exception:
            return False

    async def get_url(self, storage_path: str, expires_in: int = 3600) -> str:
        try:
            response = self._client.storage.from_(self._bucket).create_signed_url(
                storage_path, expires_in
            )
            return response.get("signedURL", "")
        except Exception as e:
            from app.utils.exceptions import StorageError
            raise StorageError(f"Failed to generate URL: {e}")


# ---------------------------------------------------------------------------
# Local Storage Provider (development / testing)
# ---------------------------------------------------------------------------

class LocalStorageProvider(StorageProvider):
    """
    Stores files on the local filesystem.
    NOT suitable for production or multi-instance deployments.
    """

    def __init__(self, base_path: str = settings.LOCAL_STORAGE_PATH) -> None:
        self._base = Path(base_path)
        self._base.mkdir(parents=True, exist_ok=True)

    def _full_path(self, storage_path: str) -> Path:
        # Prevent path traversal
        full = (self._base / storage_path).resolve()
        if not str(full).startswith(str(self._base.resolve())):
            raise ValueError("Invalid storage path.")
        return full

    async def upload(self, content: bytes, storage_path: str, mime_type: str) -> str:
        path = self._full_path(storage_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return storage_path

    async def download(self, storage_path: str) -> bytes:
        path = self._full_path(storage_path)
        if not path.exists():
            from app.utils.exceptions import StorageError
            raise StorageError(f"File not found: {storage_path}")
        return path.read_bytes()

    async def delete(self, storage_path: str) -> bool:
        path = self._full_path(storage_path)
        if path.exists():
            path.unlink()
            return True
        return False

    async def exists(self, storage_path: str) -> bool:
        return self._full_path(storage_path).exists()

    async def get_url(self, storage_path: str, expires_in: int = 3600) -> str:
        # In local mode, return a path-based URL
        return f"/api/v1/documents/file/{storage_path}"


# ---------------------------------------------------------------------------
# Storage Service Factory
# ---------------------------------------------------------------------------

def _generate_storage_path(
    organization_id: str,
    case_id: Optional[str],
    original_filename: str,
) -> str:
    """
    Generate a secure, unique storage path.
    NEVER uses the user-provided filename as the actual path.
    Format: {org_id}/{case_id_or_general}/{uuid4}.{ext}
    """
    ext = Path(original_filename).suffix.lower() or ".bin"
    file_uuid = uuid.uuid4()
    case_segment = case_id if case_id else "general"
    return f"{organization_id}/{case_segment}/{file_uuid}{ext}"


class StorageService:
    """
    Facade over storage providers.
    Business code should use this class — not provider classes directly.
    """

    _provider: Optional[StorageProvider] = None

    @classmethod
    def get_provider(cls) -> StorageProvider:
        if cls._provider is None:
            provider_name = settings.STORAGE_PROVIDER.upper()
            if provider_name == "SUPABASE":
                cls._provider = SupabaseStorageProvider()
            elif provider_name == "LOCAL":
                cls._provider = LocalStorageProvider()
            else:
                logger.warning(
                    "storage.unknown_provider",
                    provider=provider_name,
                    fallback="LOCAL",
                )
                cls._provider = LocalStorageProvider()
        return cls._provider

    @classmethod
    async def upload_document(
        cls,
        content: bytes,
        organization_id: str,
        case_id: Optional[str],
        original_filename: str,
        mime_type: str,
    ) -> str:
        """Upload a document and return its storage path."""
        storage_path = _generate_storage_path(organization_id, case_id, original_filename)
        provider = cls.get_provider()
        return await provider.upload(content, storage_path, mime_type)

    @classmethod
    async def download(cls, storage_path: str) -> bytes:
        return await cls.get_provider().download(storage_path)

    @classmethod
    async def delete(cls, storage_path: str) -> bool:
        return await cls.get_provider().delete(storage_path)

    @classmethod
    async def get_url(cls, storage_path: str, expires_in: int = 3600) -> str:
        return await cls.get_provider().get_url(storage_path, expires_in)
