"""
JurisPulse — Users Router
===========================
Routes: /api/v1/users/*
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser, require_firm_admin
from app.modules.auth.models import User
from app.modules.auth.schemas import UserProfile
from app.core.config.constants import UserRole
from app.database.session import get_db
from app.utils.exceptions import ForbiddenError, NotFoundError
from app.utils.pagination import PaginationParams, get_pagination_params
from app.utils.responses import paginated_response, success_response

users_router = APIRouter()


@users_router.get(
    "",
    summary="List users in the organization",
)
async def list_users(
    current_user: User = Depends(CurrentUser),
    pagination: PaginationParams = Depends(get_pagination_params),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_firm_admin()),
):
    """List all users in the current user's organization (FIRM_ADMIN+)."""
    if not current_user.organization_id and not current_user.is_superuser:
        raise ForbiddenError("No organization context.")

    query = select(User).where(
        User.organization_id == current_user.organization_id,
        User.is_active == True,
    )
    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar_one()

    result = await db.execute(
        query.offset(pagination.offset).limit(pagination.limit)
    )
    users = result.scalars().all()
    data = [UserProfile.model_validate(u).model_dump() for u in users]
    return paginated_response(data, total, pagination.page, pagination.page_size)


@users_router.get(
    "/{user_id}",
    summary="Get user by ID",
)
async def get_user(
    user_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Get a user's profile by ID. Can only view users in the same organization."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise NotFoundError("User", str(user_id))

    # Org isolation: only allow if same org, or superadmin
    if (
        not current_user.is_superuser
        and user.organization_id != current_user.organization_id
    ):
        raise NotFoundError("User", str(user_id))  # Return 404 not 403 to avoid enumeration

    return success_response(data=UserProfile.model_validate(user).model_dump())


@users_router.patch(
    "/{user_id}",
    summary="Update user profile",
)
async def update_user(
    user_id: uuid.UUID,
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
    bio: Optional[str] = None,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Update a user profile. Users can only update their own profile."""
    if current_user.id != user_id and not current_user.is_superuser:
        raise ForbiddenError("You can only update your own profile.")

    updates = {}
    if full_name is not None:
        updates["full_name"] = full_name
    if phone is not None:
        updates["phone"] = phone
    if bio is not None:
        updates["bio"] = bio

    if updates:
        await db.execute(update(User).where(User.id == user_id).values(**updates))

    result = await db.execute(select(User).where(User.id == user_id))
    updated_user = result.scalar_one_or_none()
    return success_response(
        data=UserProfile.model_validate(updated_user).model_dump(),
        message="Profile updated.",
    )
