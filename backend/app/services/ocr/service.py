"""
JurisPulse — OCR Service (Tesseract)
=======================================
Extracts text from PDF and image files using Tesseract OCR.

Design principles:
  - Does NOT pretend OCR is perfect — always tracks confidence and errors
  - Supports multi-page PDFs (page numbers preserved)
  - Accepts PDF (via pdf2image) and direct images (via pytesseract)
  - Returns structured result with per-page data

IMPORTANT: pytesseract requires the Tesseract binary to be installed.
  Linux: apt-get install tesseract-ocr tesseract-ocr-hin
  Mac: brew install tesseract
  Windows: install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki
"""

import io
import os
import tempfile
from dataclasses import dataclass, field
from typing import List, Optional

import structlog

from app.core.config.constants import OCRStatus
from app.core.config.settings import settings

logger = structlog.get_logger("jurispulse.ocr")


@dataclass
class OCRPageResult:
    """OCR result for a single page."""
    page_number: int
    text: str
    confidence: Optional[float]  # 0.0–100.0; None if unavailable
    word_count: int
    char_count: int


@dataclass
class OCRResult:
    """Complete OCR result for a document."""
    status: str  # OCRStatus value
    pages: List[OCRPageResult] = field(default_factory=list)
    full_text: str = ""
    total_pages: int = 0
    average_confidence: Optional[float] = None
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.status == OCRStatus.COMPLETED.value


class OCRService:
    """
    Tesseract-based OCR service.
    Accepts PDF files (converted via pdf2image) and image files.
    """

    @staticmethod
    def _extract_from_image(image, language: str) -> OCRPageResult:
        """Run Tesseract on a single PIL image."""
        try:
            import pytesseract
            from pytesseract import Output
            import pandas as pd

            # Get detailed data to compute confidence
            data = pytesseract.image_to_data(
                image,
                lang=language,
                output_type=Output.DICT,
            )

            # Compute mean confidence (exclude -1 which is non-word data)
            confidences = [
                c for c in data.get("conf", []) if isinstance(c, (int, float)) and c >= 0
            ]
            avg_conf = sum(confidences) / len(confidences) if confidences else None

            text = pytesseract.image_to_string(image, lang=language)

            return OCRPageResult(
                page_number=1,  # caller overrides this
                text=text,
                confidence=round(avg_conf, 2) if avg_conf is not None else None,
                word_count=len(text.split()),
                char_count=len(text),
            )
        except Exception as e:
            return OCRPageResult(
                page_number=1,
                text="",
                confidence=None,
                word_count=0,
                char_count=0,
            )

    @staticmethod
    async def extract_text(
        content: bytes,
        mime_type: str,
        language: Optional[str] = None,
    ) -> OCRResult:
        """
        Main OCR entry point.
        Dispatches to PDF or image extraction based on MIME type.
        """
        lang = language or settings.OCR_LANGUAGE

        try:
            if mime_type == "application/pdf":
                return await OCRService._extract_from_pdf(content, lang)
            elif mime_type in ("image/jpeg", "image/png", "image/tiff"):
                return await OCRService._extract_from_image_bytes(content, lang)
            else:
                return OCRResult(
                    status=OCRStatus.SKIPPED.value,
                    error=f"MIME type '{mime_type}' does not require OCR.",
                )
        except Exception as e:
            logger.error("ocr.failed", error=str(e), mime_type=mime_type)
            return OCRResult(
                status=OCRStatus.FAILED.value,
                error=str(e),
            )

    @staticmethod
    async def _extract_from_pdf(content: bytes, language: str) -> OCRResult:
        """Convert PDF pages to images then run Tesseract."""
        try:
            from pdf2image import convert_from_bytes

            images = convert_from_bytes(
                content,
                dpi=settings.OCR_DPI,
            )
        except Exception as e:
            return OCRResult(
                status=OCRStatus.FAILED.value,
                error=f"PDF conversion failed: {e}",
            )

        pages: List[OCRPageResult] = []
        for i, image in enumerate(images, start=1):
            page_result = OCRService._extract_from_image(image, language)
            page_result.page_number = i
            pages.append(page_result)

        return OCRService._build_result(pages)

    @staticmethod
    async def _extract_from_image_bytes(content: bytes, language: str) -> OCRResult:
        """OCR a single image."""
        from PIL import Image

        image = Image.open(io.BytesIO(content))
        page_result = OCRService._extract_from_image(image, language)
        page_result.page_number = 1
        return OCRService._build_result([page_result])

    @staticmethod
    def _build_result(pages: List[OCRPageResult]) -> OCRResult:
        full_text = "\n\n".join(p.text for p in pages)
        confidences = [p.confidence for p in pages if p.confidence is not None]
        avg_conf = round(sum(confidences) / len(confidences), 2) if confidences else None

        return OCRResult(
            status=OCRStatus.COMPLETED.value,
            pages=pages,
            full_text=full_text,
            total_pages=len(pages),
            average_confidence=avg_conf,
        )
