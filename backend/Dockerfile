# =============================================================================
# JurisPulse Backend — Dockerfile
# =============================================================================
# Multi-stage build:
#   Stage 1 (builder): install Python dependencies
#   Stage 2 (runtime): minimal production image
#
# The AI service containers are SEPARATE — this image contains no model weights.
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Build dependencies
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# System libraries required for:
#   - asyncpg (PostgreSQL)
#   - Pillow + pdf2image (image processing)
#   - python-magic (libmagic)
#   - pytesseract (Tesseract wrapper — tesseract itself installed in runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libmagic1 \
    libmagic-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---------------------------------------------------------------------------
# Stage 2: Runtime image
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

LABEL org.opencontainers.image.title="JurisPulse Backend"
LABEL org.opencontainers.image.description="FastAPI backend for the JurisPulse legal platform"
LABEL org.opencontainers.image.version="1.0.0"

# Non-root user for security
RUN groupadd --gid 1001 jurispulse && \
    useradd --uid 1001 --gid jurispulse --shell /bin/bash --create-home jurispulse

WORKDIR /app

# System runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libmagic1 \
    tesseract-ocr \
    tesseract-ocr-hin \
    poppler-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY --chown=jurispulse:jurispulse . .

# Create storage directory (used when STORAGE_PROVIDER=LOCAL)
RUN mkdir -p /app/storage && chown jurispulse:jurispulse /app/storage

USER jurispulse

EXPOSE 8000

# Health check for Docker
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Start Uvicorn with production settings
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "4", \
     "--log-level", "info", \
     "--no-access-log"]
