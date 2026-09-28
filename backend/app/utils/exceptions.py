"""
JurisPulse — Custom Application Exceptions
============================================
Define domain-specific exceptions here.
All exceptions are mapped to HTTP responses in the exception handlers
registered in main.py. Route handlers should raise these exceptions;
they should never manually construct error JSONResponse objects.

Error code conventions:
  AUTH_*          Authentication / authorisation
  VALIDATION_*    Input validation failures
  NOT_FOUND_*     Resource not found
  CONFLICT_*      Duplicate / constraint violations
  FORBIDDEN_*     Permission denied
  AI_*            AI service errors
  STORAGE_*       File storage errors
  OCR_*           OCR processing errors
  WORKFLOW_*      Workflow engine errors
  RATE_LIMIT_*    Rate limiting
  INTERNAL_*      Unexpected internal errors
"""

from typing import Any, Optional


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

class JurisPulseError(Exception):
    """Base exception for all application errors."""

    http_status_code: int = 500
    error_code: str = "INTERNAL_ERROR"

    def __init__(
        self,
        message: str = "An unexpected error occurred.",
        details: Optional[dict[str, Any]] = None,
    ) -> None:
        self.message = message
        self.details = details or {}
        super().__init__(message)


# ---------------------------------------------------------------------------
# Authentication & Authorisation
# ---------------------------------------------------------------------------

class AuthenticationError(JurisPulseError):
    http_status_code = 401
    error_code = "AUTH_FAILED"

    def __init__(self, message: str = "Authentication failed.") -> None:
        super().__init__(message)


class InvalidTokenError(JurisPulseError):
    http_status_code = 401
    error_code = "AUTH_INVALID_TOKEN"

    def __init__(self, message: str = "Invalid or expired token.") -> None:
        super().__init__(message)


class TokenExpiredError(JurisPulseError):
    http_status_code = 401
    error_code = "AUTH_TOKEN_EXPIRED"

    def __init__(self, message: str = "Token has expired.") -> None:
        super().__init__(message)


class ForbiddenError(JurisPulseError):
    http_status_code = 403
    error_code = "FORBIDDEN"

    def __init__(
        self,
        message: str = "You do not have permission to perform this action.",
    ) -> None:
        super().__init__(message)


class InsufficientPermissionsError(ForbiddenError):
    error_code = "FORBIDDEN_INSUFFICIENT_PERMISSIONS"

    def __init__(
        self,
        required: Optional[str] = None,
        message: Optional[str] = None,
    ) -> None:
        msg = message or (
            f"Insufficient permissions. Required: {required}."
            if required
            else "Insufficient permissions."
        )
        super().__init__(msg)


class OrganizationAccessDeniedError(ForbiddenError):
    error_code = "FORBIDDEN_ORGANIZATION"

    def __init__(self) -> None:
        super().__init__("Access to this organization's resources is denied.")


# ---------------------------------------------------------------------------
# Resource Not Found
# ---------------------------------------------------------------------------

class NotFoundError(JurisPulseError):
    http_status_code = 404
    error_code = "NOT_FOUND"

    def __init__(self, resource: str = "Resource", id: Optional[str] = None) -> None:
        msg = f"{resource} not found."
        if id:
            msg = f"{resource} with id '{id}' not found."
        super().__init__(msg, {"resource": resource, "id": id})


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class ValidationError(JurisPulseError):
    http_status_code = 422
    error_code = "VALIDATION_ERROR"

    def __init__(
        self,
        message: str = "Validation failed.",
        field: Optional[str] = None,
        details: Optional[dict] = None,
    ) -> None:
        d = details or {}
        if field:
            d["field"] = field
        super().__init__(message, d)


# ---------------------------------------------------------------------------
# Conflict
# ---------------------------------------------------------------------------

class ConflictError(JurisPulseError):
    http_status_code = 409
    error_code = "CONFLICT"

    def __init__(self, message: str = "Resource already exists.") -> None:
        super().__init__(message)


class DuplicateEmailError(ConflictError):
    error_code = "CONFLICT_DUPLICATE_EMAIL"

    def __init__(self) -> None:
        super().__init__("A user with this email address already exists.")


# ---------------------------------------------------------------------------
# Rate Limiting
# ---------------------------------------------------------------------------

class RateLimitError(JurisPulseError):
    http_status_code = 429
    error_code = "RATE_LIMIT_EXCEEDED"

    def __init__(self, message: str = "Too many requests. Please slow down.") -> None:
        super().__init__(message)


# ---------------------------------------------------------------------------
# File / Storage
# ---------------------------------------------------------------------------

class StorageError(JurisPulseError):
    http_status_code = 500
    error_code = "STORAGE_ERROR"


class FileValidationError(JurisPulseError):
    http_status_code = 400
    error_code = "VALIDATION_FILE"

    def __init__(self, message: str, details: Optional[dict] = None) -> None:
        super().__init__(message, details)


class FileTooLargeError(FileValidationError):
    error_code = "VALIDATION_FILE_TOO_LARGE"

    def __init__(self, max_mb: int = 50) -> None:
        super().__init__(f"File exceeds the maximum allowed size of {max_mb} MB.")


class UnsupportedFileTypeError(FileValidationError):
    error_code = "VALIDATION_FILE_TYPE"

    def __init__(self, mime_type: str = "") -> None:
        super().__init__(
            f"Unsupported file type: '{mime_type}'. Upload PDF, images, or Word documents.",
            {"mime_type": mime_type},
        )


# ---------------------------------------------------------------------------
# OCR
# ---------------------------------------------------------------------------

class OCRError(JurisPulseError):
    http_status_code = 500
    error_code = "OCR_ERROR"


# ---------------------------------------------------------------------------
# AI / Model
# ---------------------------------------------------------------------------

class AIServiceError(JurisPulseError):
    http_status_code = 502
    error_code = "AI_SERVICE_ERROR"


class ModelUnavailableError(AIServiceError):
    error_code = "AI_MODEL_UNAVAILABLE"

    def __init__(self, model_name: str = "AI model") -> None:
        super().__init__(
            f"The {model_name} is currently unavailable. Please try again later."
        )


class ModelNotDeployedError(AIServiceError):
    http_status_code = 503
    error_code = "AI_MODEL_NOT_DEPLOYED"

    def __init__(self, model_name: str = "AI model") -> None:
        super().__init__(
            f"The {model_name} has not been deployed yet. This feature is not available."
        )


class EmbeddingServiceError(AIServiceError):
    error_code = "AI_EMBEDDING_ERROR"


class DraftingServiceError(AIServiceError):
    error_code = "AI_DRAFTING_ERROR"


class VerificationServiceError(AIServiceError):
    error_code = "AI_VERIFICATION_ERROR"


# ---------------------------------------------------------------------------
# Workflow
# ---------------------------------------------------------------------------

class WorkflowError(JurisPulseError):
    http_status_code = 500
    error_code = "WORKFLOW_ERROR"


class WorkflowNotFoundError(NotFoundError):
    def __init__(self, workflow_id: Optional[str] = None) -> None:
        super().__init__("Workflow", workflow_id)


class WorkflowAlreadyRunningError(ConflictError):
    error_code = "CONFLICT_WORKFLOW_RUNNING"

    def __init__(self) -> None:
        super().__init__("A workflow for this case is already running.")


# ---------------------------------------------------------------------------
# Case
# ---------------------------------------------------------------------------

class CaseAccessDeniedError(ForbiddenError):
    error_code = "FORBIDDEN_CASE_ACCESS"

    def __init__(self) -> None:
        super().__init__("You do not have access to this case.")


class CaseNotFoundError(NotFoundError):
    def __init__(self, case_id: Optional[str] = None) -> None:
        super().__init__("Case", case_id)
