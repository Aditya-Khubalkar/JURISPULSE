"""
JurisPulse — Application Settings
===================================
Centralised configuration using Pydantic v2 BaseSettings.
All values must come from environment variables or .env file.
Never hard-code secrets in this file.
"""

from functools import lru_cache
from typing import List, Optional

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # -----------------------------------------------------------------------
    # Application
    # -----------------------------------------------------------------------
    APP_NAME: str = "JurisPulse"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = False

    # -----------------------------------------------------------------------
    # API
    # -----------------------------------------------------------------------
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_HOSTS: List[str] = ["*"]

    # -----------------------------------------------------------------------
    # Database (PostgreSQL async)
    # -----------------------------------------------------------------------
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 1800  # seconds

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        # Ensure async driver is used
        if v.startswith("postgresql://"):
            v = v.replace("postgresql://", "postgresql+psycopg://", 1)
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql+psycopg://", 1)
        # Handle case where user provides asyncpg in URL but we use psycopg
        if v.startswith("postgresql+asyncpg://"):
            v = v.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
        return v

    # -----------------------------------------------------------------------
    # Redis
    # -----------------------------------------------------------------------
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    REDIS_RATE_LIMIT_DB: int = 3

    # -----------------------------------------------------------------------
    # Supabase
    # -----------------------------------------------------------------------
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_JWT_SECRET: str  # Used to verify Supabase-issued JWTs

    # -----------------------------------------------------------------------
    # JWT (for any locally issued tokens — e.g. internal service tokens)
    # -----------------------------------------------------------------------
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # -----------------------------------------------------------------------
    # CORS
    # -----------------------------------------------------------------------
    CORS_ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOWED_METHODS: List[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    CORS_ALLOWED_HEADERS: List[str] = ["*"]

    # -----------------------------------------------------------------------
    # Rate Limiting
    # -----------------------------------------------------------------------
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    RATE_LIMIT_BURST: int = 20

    # -----------------------------------------------------------------------
    # Storage
    # -----------------------------------------------------------------------
    STORAGE_PROVIDER: str = "SUPABASE"  # SUPABASE | LOCAL | MINIO | S3
    STORAGE_BUCKET: str = "jurispulse-documents"
    LOCAL_STORAGE_PATH: str = "./storage"
    MINIO_ENDPOINT: Optional[str] = None
    MINIO_ACCESS_KEY: Optional[str] = None
    MINIO_SECRET_KEY: Optional[str] = None
    MINIO_SECURE: bool = False

    # -----------------------------------------------------------------------
    # File Upload
    # -----------------------------------------------------------------------
    MAX_FILE_SIZE_MB: int = 50
    MAX_FILE_SIZE_BYTES: int = 52_428_800  # 50 MB in bytes

    @model_validator(mode="after")
    def sync_file_size(self) -> "Settings":
        self.MAX_FILE_SIZE_BYTES = self.MAX_FILE_SIZE_MB * 1024 * 1024
        return self

    # -----------------------------------------------------------------------
    # OCR
    # -----------------------------------------------------------------------
    OCR_ENGINE: str = "tesseract"
    OCR_LANGUAGE: str = "eng+hin"
    OCR_DPI: int = 300

    # -----------------------------------------------------------------------
    # AI Service URLs (backend calls these; models are NOT loaded here)
    # -----------------------------------------------------------------------
    AI_DRAFTER_URL: str = "http://localhost:8001"
    AI_EMBEDDING_URL: str = "http://localhost:8002"
    AI_VERIFICATION_URL: str = "http://localhost:8003"

    # Timeout in seconds for AI service calls
    AI_SERVICE_TIMEOUT: int = 120
    AI_HEALTH_CHECK_TIMEOUT: int = 10
    AI_HEALTH_CHECK_INTERVAL: int = 60  # seconds between health polls

    # -----------------------------------------------------------------------
    # Vector Search (Supabase pgvector)
    # -----------------------------------------------------------------------
    VECTOR_SEARCH_TABLE: str = "legal_chunks"
    VECTOR_SEARCH_FUNCTION: str = "match_legal_chunks"
    EMBEDDING_DIMENSION: int = 384  # bge-small output dimension
    DEFAULT_SEARCH_LIMIT: int = 10
    MAX_SEARCH_LIMIT: int = 50

    # -----------------------------------------------------------------------
    # Celery / Workers
    # -----------------------------------------------------------------------
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_TIMEZONE: str = "Asia/Kolkata"
    CELERY_TASK_TRACK_STARTED: bool = True
    CELERY_TASK_TIME_LIMIT: int = 3600       # 1 hour hard limit
    CELERY_TASK_SOFT_TIME_LIMIT: int = 3300  # 55 min soft limit

    # -----------------------------------------------------------------------
    # Logging
    # -----------------------------------------------------------------------
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json | text
    LOG_SENSITIVE_FIELDS: List[str] = [
        "password",
        "token",
        "secret",
        "key",
        "authorization",
    ]

    # -----------------------------------------------------------------------
    # Pagination
    # -----------------------------------------------------------------------
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # -----------------------------------------------------------------------
    # Security Headers
    # -----------------------------------------------------------------------
    SECURITY_HEADERS_ENABLED: bool = True
    CONTENT_SECURITY_POLICY: str = "default-src 'self'"

    # -----------------------------------------------------------------------
    # Feature Flags
    # -----------------------------------------------------------------------
    ENABLE_HALLUCINATION_DETECTION: bool = False  # model NOT_DEPLOYED
    ENABLE_NER: bool = False                       # future model
    ENABLE_AUTO_CLASSIFICATION: bool = False       # future model
    ENABLE_RISK_ASSESSMENT: bool = False           # future model

    # -----------------------------------------------------------------------
    # Audit
    # -----------------------------------------------------------------------
    AUDIT_LOG_ENABLED: bool = True
    AUDIT_LOG_RETENTION_DAYS: int = 365


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance. Call this via dependency injection."""
    return Settings()


# Module-level singleton for non-DI usage (config, migrations, etc.)
settings: Settings = get_settings()
