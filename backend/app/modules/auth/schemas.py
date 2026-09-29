"""
JurisPulse — Auth Schemas (Pydantic v2)
==========================================
Request and response schemas for authentication endpoints.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

class RegisterRequest(BaseModel):
    """Request body for new user registration via Supabase Auth."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)

    @model_validator(mode="after")
    def validate_password_strength(self) -> "RegisterRequest":
        password = self.password
        errors = []
        if not any(c.isupper() for c in password):
            errors.append("at least one uppercase letter")
        if not any(c.isdigit() for c in password):
            errors.append("at least one digit")
        if errors:
            raise ValueError(f"Password must contain {' and '.join(errors)}.")
        return self


class RegisterResponse(BaseModel):
    """Response after successful registration."""

    user_id: uuid.UUID
    email: EmailStr
    full_name: str
    message: str = "Registration successful. Please verify your email."


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    """Supabase Auth login credentials."""

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenPair(BaseModel):
    """Access + refresh token pair returned on successful login."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class LoginResponse(BaseModel):
    """Full login response including tokens and user info."""

    tokens: TokenPair
    user: "UserProfile"


# ---------------------------------------------------------------------------
# Token Refresh
# ---------------------------------------------------------------------------

class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# ---------------------------------------------------------------------------
# Password Reset
# ---------------------------------------------------------------------------

class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


# ---------------------------------------------------------------------------
# User Profile (reused in multiple responses)
# ---------------------------------------------------------------------------

class UserProfile(BaseModel):
    """Serialised user profile returned to the client."""

    model_config = {"from_attributes": True}

    id: uuid.UUID
    email: str
    full_name: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    is_verified: bool
    organization_id: Optional[uuid.UUID] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime


# Rebuild the forward reference
LoginResponse.model_rebuild()
