"""
JurisPulse — Auth FastAPI Dependencies
=========================================
These dependencies are used in route handlers to:
  1. Extract and verify the bearer token from the Authorization header.
  2. Load the current user from the database.
  3. Enforce role-based access control.

Usage in a router::

    @router.get("/example")
    async def example(
        current_user: User = Depends(get_current_user),
        _: None = Depends(require_role(UserRole.SENIOR_LAWYER)),
    ):
        ...
"""

import uuid
from typing import Annotated, Optional

import structlog
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import User
from app.modules.auth.security import verify_supabase_token, extract_supabase_user_id
from app.core.config.constants import UserRole
from app.database.session import get_db
from app.utils.exceptions import (
    AuthenticationError,
    ForbiddenError,
    InsufficientPermissionsError,
    InvalidTokenError,
    TokenExpiredError,
)

logger = structlog.get_logger("jurispulse.auth.dependencies")


# ---------------------------------------------------------------------------
# Token extraction
# ---------------------------------------------------------------------------

async def _extract_bearer_token(
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> str:
    """Extract the raw JWT from the Authorization: Bearer <token> header."""
    if not authorization:
        raise AuthenticationError("Authorization header is missing.")
    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise AuthenticationError("Invalid authorization header format. Use 'Bearer <token>'.")
    token = parts[1].strip()
    if not token:
        raise AuthenticationError("Authorization token is empty.")
    return token


# ---------------------------------------------------------------------------
# Current user dependency
# ---------------------------------------------------------------------------

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(_extract_bearer_token),
) -> User:
    """
    FastAPI dependency that:
    1. Verifies the Supabase JWT.
    2. Loads the matching User record from the database.
    3. Checks that the user is active.

    Raises AuthenticationError (401) if any step fails.
    """
    try:
        payload = verify_supabase_token(token)
        supabase_user_id = extract_supabase_user_id(payload)
    except (InvalidTokenError, TokenExpiredError) as exc:
        raise exc  # Already typed exceptions

    result = await db.execute(
        select(User).where(
            User.supabase_user_id == supabase_user_id,
            User.is_active == True,
        )
    )
    user = result.scalar_one_or_none()

    if user is None:
        logger.warning(
            "auth.user_not_found",
            supabase_user_id=supabase_user_id,
        )
        raise AuthenticationError("User account not found or is inactive.")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Alias for get_current_user — kept for explicitness in sensitive routes."""
    if not current_user.is_active:
        raise AuthenticationError("Account is deactivated.")
    return current_user


# ---------------------------------------------------------------------------
# Optional auth (for public endpoints that show richer data when logged in)
# ---------------------------------------------------------------------------

async def get_current_user_optional(
    db: AsyncSession = Depends(get_db),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> Optional[User]:
    """Returns the current user if authenticated, or None for anonymous access."""
    if not authorization:
        return None
    try:
        parts = authorization.split(" ", 1)
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        token = parts[1].strip()
        payload = verify_supabase_token(token)
        supabase_user_id = extract_supabase_user_id(payload)
        result = await db.execute(
            select(User).where(
                User.supabase_user_id == supabase_user_id,
                User.is_active == True,
            )
        )
        return result.scalar_one_or_none()
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Role-based access control
# ---------------------------------------------------------------------------

_ROLE_HIERARCHY = {
    UserRole.SUPER_ADMIN: 100,
    UserRole.FIRM_ADMIN: 80,
    UserRole.SENIOR_LAWYER: 60,
    UserRole.JUNIOR_LAWYER: 50,
    UserRole.PARALEGAL: 40,
    UserRole.RESEARCHER: 30,
    UserRole.CLIENT: 20,
    UserRole.GUEST: 10,
}


def require_role(*allowed_roles: UserRole):
    """
    FastAPI dependency factory.
    Raises ForbiddenError (403) if the user's highest role is not in allowed_roles.

    Usage::
        @router.post("/admin")
        async def admin_endpoint(
            _: None = Depends(require_role(UserRole.FIRM_ADMIN, UserRole.SUPER_ADMIN)),
            current_user: User = Depends(get_current_user),
        ):
            ...
    """
    allowed_set = set(allowed_roles)

    async def _check_role(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
    ) -> None:
        from app.modules.roles.service import RoleService
        user_roles = await RoleService.get_user_role_names(db, current_user.id)

        if current_user.is_superuser:
            return  # Super admin bypasses all role checks

        if not any(role in allowed_set for role in user_roles):
            raise InsufficientPermissionsError(
                required=", ".join(r.value for r in allowed_roles)
            )

    return _check_role


def require_superadmin():
    """Dependency that only allows SUPER_ADMIN users."""
    return require_role(UserRole.SUPER_ADMIN)


def require_firm_admin():
    """Dependency that allows FIRM_ADMIN and SUPER_ADMIN."""
    return require_role(UserRole.FIRM_ADMIN, UserRole.SUPER_ADMIN)


# ---------------------------------------------------------------------------
# Typed dependency aliases for cleaner route signatures
# ---------------------------------------------------------------------------

CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentUserOptional = Annotated[Optional[User], Depends(get_current_user_optional)]
