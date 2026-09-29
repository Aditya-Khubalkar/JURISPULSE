"""
JurisPulse — Authentication Security Utilities
================================================
Supabase JWT verification and user identity extraction.

Authentication authority: Supabase Auth.
This module:
  1. Verifies JWT signatures using the Supabase JWT secret.
  2. Extracts the sub (user ID) and email claims.
  3. Does NOT issue new JWTs — that is Supabase's responsibility.

If locally signed JWTs are ever needed (e.g., internal tokens), a
separate utility is included at the bottom of this file.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import structlog
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config.settings import settings
from app.utils.exceptions import InvalidTokenError, TokenExpiredError

logger = structlog.get_logger("jurispulse.auth.security")

# ---------------------------------------------------------------------------
# Password hashing (used only for locally created accounts, if ever needed)
# ---------------------------------------------------------------------------

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Hash a plain-text password using bcrypt."""
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against its bcrypt hash."""
    return _pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------------------------
# Supabase JWT verification
# ---------------------------------------------------------------------------

def verify_supabase_token(token: str) -> dict[str, Any]:
    """
    Verify a Supabase-issued JWT.

    Returns the decoded payload (claims) on success.
    Raises InvalidTokenError or TokenExpiredError on failure.

    The Supabase JWT secret is used for HMAC-SHA256 verification.
    Algorithm: HS256 (Supabase default).
    """
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False},  # Supabase doesn't set aud by default
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except JWTError as e:
        logger.debug("supabase_token_invalid", error=str(e))
        raise InvalidTokenError()


def extract_supabase_user_id(payload: dict[str, Any]) -> str:
    """Extract the user ID (sub claim) from a decoded Supabase JWT payload."""
    sub = payload.get("sub")
    if not sub:
        raise InvalidTokenError("Token is missing required claims.")
    return str(sub)


def extract_supabase_email(payload: dict[str, Any]) -> Optional[str]:
    """Extract the email claim from a decoded Supabase JWT payload."""
    return payload.get("email")


# ---------------------------------------------------------------------------
# Internal / local JWT utilities (for service-to-service tokens, NOT auth)
# ---------------------------------------------------------------------------

def create_internal_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
    extra_claims: Optional[dict[str, Any]] = None,
) -> str:
    """
    Create a short-lived JWT for internal service communication.
    This is NOT a user authentication token.
    """
    now = datetime.now(timezone.utc)
    exp = now + (expires_delta or timedelta(minutes=15))
    payload = {
        "sub": subject,
        "iat": now,
        "exp": exp,
        "type": "internal",
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_internal_token(token: str) -> dict[str, Any]:
    """Decode and verify an internal service JWT."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        if payload.get("type") != "internal":
            raise InvalidTokenError("Not an internal token.")
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except JWTError:
        raise InvalidTokenError()
