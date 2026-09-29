"""
JurisPulse — Organizations Router
=====================================
Routes: /api/v1/organizations/*
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser, require_firm_admin, require_superadmin
from app.modules.auth.models import User
from app.database.session import get_db
from app.modules.organizations.models import Organization
from app.utils.exceptions import ForbiddenError, NotFoundError
from app.utils.responses import created_response, success_response

organizations_router = APIRouter()


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    slug: str = Field(min_length=2, max_length=100, pattern=r"^[a-z0-9\-]+$")
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None


class OrganizationRead(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    name: str
    slug: str
    description: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    city: Optional[str]
    state: Optional[str]
    is_active: bool


@organizations_router.post(
    "",
    summary="Create organization (Super Admin only)",
    status_code=201,
)
async def create_organization(
    body: OrganizationCreate,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_superadmin()),
):
    """Create a new law firm organization. Super Admin only."""
    # Check slug uniqueness
    existing = await db.execute(
        select(Organization).where(Organization.slug == body.slug)
    )
    if existing.scalar_one_or_none():
        from app.utils.exceptions import ConflictError
        raise ConflictError(f"An organization with slug '{body.slug}' already exists.")

    org = Organization(**body.model_dump())
    db.add(org)
    await db.flush()
    await db.refresh(org)

    return created_response(
        data=OrganizationRead.model_validate(org).model_dump(),
        message="Organization created.",
    )


@organizations_router.get(
    "/me",
    summary="Get current user's organization",
)
async def get_my_organization(
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Return the organization the current user belongs to."""
    if not current_user.organization_id:
        raise NotFoundError("Organization")

    result = await db.execute(
        select(Organization).where(Organization.id == current_user.organization_id)
    )
    org = result.scalar_one_or_none()
    if not org:
        raise NotFoundError("Organization")

    return success_response(data=OrganizationRead.model_validate(org).model_dump())


@organizations_router.get(
    "/{org_id}",
    summary="Get organization by ID (Admin+)",
)
async def get_organization(
    org_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Get an organization by ID. Users can only view their own organization."""
    if not current_user.is_superuser and current_user.organization_id != org_id:
        raise ForbiddenError("Access denied to this organization.")

    result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalar_one_or_none()
    if not org:
        raise NotFoundError("Organization", str(org_id))

    return success_response(data=OrganizationRead.model_validate(org).model_dump())
