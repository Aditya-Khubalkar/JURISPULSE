"""
JurisPulse — Auth Service
===========================
Business logic for authentication operations.

All auth operations go through Supabase Auth.
This service calls the Supabase client for registration/login,
then syncs the result into the local users table.
"""

import structlog
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from supabase import Client as SupabaseClient, create_client

from app.modules.auth.models import User
from app.modules.auth.schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse,
    TokenPair,
    UserProfile,
)
from app.core.config.settings import settings
from app.utils.exceptions import (
    AuthenticationError,
    ConflictError,
    DuplicateEmailError,
)

logger = structlog.get_logger("jurispulse.auth.service")


def _get_supabase_client() -> SupabaseClient:
    """Return a Supabase client using the service role key for admin operations."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


def _get_supabase_anon_client() -> SupabaseClient:
    """Return an anon Supabase client for user-facing auth (sign in, sign up)."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)


class AuthService:
    """Handles user registration, login, and token refresh via Supabase Auth."""

    @staticmethod
    async def register(
        db: AsyncSession,
        data: RegisterRequest,
        client_ip: Optional[str] = None,
    ) -> RegisterResponse:
        """
        Register a new user via Supabase Auth, then create a local User record.
        """
        # Check for duplicate email in local DB first (fast check)
        existing = await db.execute(
            select(User).where(User.email == data.email.lower())
        )
        if existing.scalar_one_or_none():
            raise DuplicateEmailError()

        # Register with Supabase Auth
        try:
            supabase = _get_supabase_anon_client()
            response = supabase.auth.sign_up(
                {
                    "email": data.email.lower(),
                    "password": data.password,
                }
            )
        except Exception as e:
            error_msg = str(e).lower()
            if "already registered" in error_msg or "already exists" in error_msg:
                raise DuplicateEmailError()
            logger.error("supabase.register_failed", error=str(e))
            raise AuthenticationError("Registration failed. Please try again.")

        if not response.user:
            raise AuthenticationError("Registration failed. Please try again.")

        supabase_user = response.user

        # Create local User record
        local_user = User(
            supabase_user_id=supabase_user.id,
            email=data.email.lower(),
            full_name=data.full_name,
            phone=data.phone,
            is_active=True,
            is_verified=False,
        )
        db.add(local_user)
        await db.flush()
        await db.refresh(local_user)

        logger.info(
            "auth.register",
            user_id=str(local_user.id),
            email=local_user.email,
        )

        return RegisterResponse(
            user_id=local_user.id,
            email=local_user.email,
            full_name=local_user.full_name,
        )

    @staticmethod
    async def login(
        db: AsyncSession,
        data: LoginRequest,
        client_ip: Optional[str] = None,
    ) -> LoginResponse:
        """
        Sign in via Supabase Auth and return an access/refresh token pair.
        Updates last_login_at on the local user record.
        """
        try:
            supabase = _get_supabase_anon_client()
            response = supabase.auth.sign_in_with_password(
                {"email": data.email.lower(), "password": data.password}
            )
        except Exception as e:
            logger.warning("auth.login_failed", email=data.email, error=str(e))
            raise AuthenticationError("Invalid email or password.")

        if not response.user or not response.session:
            raise AuthenticationError("Invalid email or password.")

        supabase_user = response.user
        session = response.session

        # Load or create local user record
        result = await db.execute(
            select(User).where(User.supabase_user_id == supabase_user.id)
        )
        local_user = result.scalar_one_or_none()

        if local_user is None:
            # Auto-provision if they exist in Supabase but not local DB
            local_user = User(
                supabase_user_id=supabase_user.id,
                email=supabase_user.email or data.email.lower(),
                full_name=supabase_user.user_metadata.get("full_name", data.email.split("@")[0]),
                is_active=True,
                is_verified=supabase_user.email_confirmed_at is not None,
            )
            db.add(local_user)
            await db.flush()

        if not local_user.is_active:
            raise AuthenticationError("Your account has been deactivated.")

        # Update last login info
        await db.execute(
            update(User)
            .where(User.id == local_user.id)
            .values(
                last_login_at=datetime.now(timezone.utc),
                last_login_ip=client_ip,
                is_verified=supabase_user.email_confirmed_at is not None,
            )
        )

        logger.info("auth.login", user_id=str(local_user.id), email=local_user.email)

        tokens = TokenPair(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            token_type="bearer",
            expires_in=session.expires_in or 3600,
        )

        profile = UserProfile.model_validate(local_user)
        return LoginResponse(tokens=tokens, user=profile)

    @staticmethod
    async def logout(refresh_token: str) -> None:
        """Sign out the user from Supabase Auth, invalidating the session."""
        try:
            supabase = _get_supabase_anon_client()
            supabase.auth.sign_out()
        except Exception as e:
            logger.warning("auth.logout_error", error=str(e))
            # Logout errors are non-fatal — token expires anyway

    @staticmethod
    async def refresh_token(refresh_token: str) -> dict:
        """Exchange a Supabase refresh token for a new access token."""
        try:
            supabase = _get_supabase_anon_client()
            response = supabase.auth.refresh_session(refresh_token)
        except Exception as e:
            logger.warning("auth.refresh_failed", error=str(e))
            raise AuthenticationError("Failed to refresh token. Please log in again.")

        if not response.session:
            raise AuthenticationError("Invalid or expired refresh token.")

        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "expires_in": response.session.expires_in or 3600,
        }

    @staticmethod
    async def request_password_reset(email: str) -> None:
        """Send a password reset email via Supabase Auth."""
        try:
            supabase = _get_supabase_anon_client()
            supabase.auth.reset_password_email(email.lower())
        except Exception as e:
            logger.warning("auth.password_reset_error", error=str(e))
        # Always return success to prevent user enumeration

    @staticmethod
    async def get_me(db: AsyncSession, user_id: str) -> Optional[User]:
        """Load the current user profile by supabase_user_id."""
        result = await db.execute(
            select(User).where(User.supabase_user_id == user_id)
        )
        return result.scalar_one_or_none()
