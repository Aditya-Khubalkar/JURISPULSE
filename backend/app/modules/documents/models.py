"""
JurisPulse — Document Models
================================
Documents, document versions, and extracted metadata.

Document lifecycle:
  UPLOADED → VALIDATING → STORED → OCR_PENDING → OCR_PROCESSING
  → OCR_COMPLETE → CLEANING → METADATA_EXTRACTION → CLASSIFYING
  → CHUNKING → EMBEDDING → INDEXING → COMPLETED (or FAILED)
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config.constants import DocumentStatus, DocumentType
from app.database.base import Base, TimestampMixin, UUIDMixin


class Document(UUIDMixin, TimestampMixin, Base):
    """
    A legal document associated with a case.
    The file is stored in cloud/local storage — this record is the metadata.
    """

    __tablename__ = "documents"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    case_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("cases.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Display name — what the user called it
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    # Sanitised original filename (for display only, NOT used as storage path)
    original_filename: Mapped[str] = mapped_column(String(500), nullable=False)
    document_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default=DocumentType.OTHER.value
    )
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    checksum: Mapped[str] = mapped_column(String(128), nullable=False, index=True)

    # Storage path — UUID-based, never derived from user input
    storage_path: Mapped[str] = mapped_column(String(1024), unique=True, nullable=False)
    storage_provider: Mapped[str] = mapped_column(String(50), nullable=False)

    status: Mapped[str] = mapped_column(
        String(50), nullable=False, default=DocumentStatus.UPLOADED.value, index=True
    )
    status_message: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    uploaded_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    current_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Extracted content
    extracted_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    page_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationships
    versions: Mapped[List["DocumentVersion"]] = relationship(
        "DocumentVersion",
        back_populates="document",
        lazy="select",
        cascade="all, delete-orphan",
    )
    metadata_records: Mapped[List["DocumentMetadata"]] = relationship(
        "DocumentMetadata",
        back_populates="document",
        lazy="select",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Document id={self.id} name={self.name} status={self.status}>"


class DocumentVersion(UUIDMixin, Base):
    """
    A version of a document.
    Created each time the document file is replaced/updated.
    """

    __tablename__ = "document_versions"

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    checksum: Mapped[str] = mapped_column(String(128), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    change_summary: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    document: Mapped["Document"] = relationship("Document", back_populates="versions")


class DocumentMetadata(UUIDMixin, Base):
    """
    Extracted metadata key-value pairs for a document.
    Populated during the document processing pipeline.
    """

    __tablename__ = "document_metadata"

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    key: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(
        String(50), nullable=False, default="ocr"
    )  # ocr | classifier | ner | manual

    document: Mapped["Document"] = relationship("Document", back_populates="metadata_records")
