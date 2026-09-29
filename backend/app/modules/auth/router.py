"""
JurisPulse — Auth Router
==========================
All authentication endpoints live here.
Routes: /api/v1/auth/*
"""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.schemas import (
    LoginRequest,
    LoginResponse,
    PasswordResetRequest,
    RefreshRequest,
    RefreshResponse,
    RegisterRequest,
    RegisterResponse,
    UserProfile,
)
from app.modules.auth.service import AuthService
from app.database.session import get_db
from app.utils.responses import created_response, success_response

auth_router = APIRouter()


@auth_router.post(
    "/register",
    summary="Register a new user",
    status_code=201,
)
async def register(
    body: RegisterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new user account.
    Registers via Supabase Auth, then creates a local profile.
    """
    result = await AuthService.register(
        db,
        body,
        client_ip=request.client.host if request.client else None,
    )
    return created_response(data=result.model_dump(), message=result.message)


@auth_router.post(
    "/login",
    response_model=None,
    summary="Login and obtain tokens",
)
async def login(
    body: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Sign in with email and password.
    Returns a Supabase access token + refresh token.
    """
    result = await AuthService.login(
        db,
        body,
        client_ip=request.client.host if request.client else None,
    )
    return success_response(data=result.model_dump(), message="Login successful.")


@auth_router.post(
    "/logout",
    summary="Logout and invalidate session",
)
async def logout(body: RefreshRequest):
    """Sign out the current user. Invalidates the Supabase session."""
    await AuthService.logout(body.refresh_token)
    return success_response(message="Logged out successfully.")


@auth_router.post(
    "/refresh",
    summary="Refresh access token",
)
async def refresh_token(body: RefreshRequest):
    """Exchange a Supabase refresh token for a new access token."""
    result = await AuthService.refresh_token(body.refresh_token)
    return success_response(data=result, message="Token refreshed.")


@auth_router.post(
    "/forgot-password",
    summary="Request password reset email",
)
async def forgot_password(body: PasswordResetRequest):
    """
    Send a password reset email.
    Always returns success to prevent user enumeration.
    """
    await AuthService.request_password_reset(body.email)
    return success_response(
        message="If an account with that email exists, a reset link has been sent."
    )


@auth_router.get(
    "/me",
    summary="Get current user profile",
    response_model=UserProfile,
)
async def get_me(current_user=Depends(CurrentUser)):
    """Return the authenticated user's profile."""
    return success_response(
        data=UserProfile.model_validate(current_user).model_dump(),
        message="User profile retrieved.",
    )
