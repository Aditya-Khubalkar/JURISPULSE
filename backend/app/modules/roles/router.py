"""
JurisPulse — Roles Router
===========================
Routes: /api/v1/roles/*
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser, require_firm_admin
from app.modules.auth.models import User
from app.database.session import get_db
from app.modules.roles.models import Permission, Role, UserRole
from app.modules.roles.service import RoleService
from app.utils.responses import success_response

roles_router = APIRouter()


class RoleRead(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    name: str
    display_name: str
    description: Optional[str]
    is_system: bool


class RoleAssignRequest(BaseModel):
    user_id: uuid.UUID
    role_name: str


@roles_router.get("", summary="List all available roles")
async def list_roles(
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Return all available roles in the system."""
    roles = await RoleService.list_all_roles(db)
    return success_response(
        data=[RoleRead.model_validate(r).model_dump() for r in roles]
    )


@roles_router.get("/permissions", summary="List all available permissions")
async def list_permissions(
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_firm_admin()),
):
    """Return all resource+action permissions."""
    permissions = await RoleService.list_permissions(db)
    return success_response(
        data=[
            {"id": str(p.id), "resource": p.resource, "action": p.action, "description": p.description}
            for p in permissions
        ]
    )


@roles_router.post("/assign", summary="Assign a role to a user")
async def assign_role(
    body: RoleAssignRequest,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_firm_admin()),
):
    """Assign a role to a user within the current user's organization."""
    assignment = await RoleService.assign_role(
        db,
        user_id=body.user_id,
        role_name=body.role_name,
        organization_id=current_user.organization_id,
        assigned_by=current_user.id,
    )
    return success_response(
        data={"assignment_id": str(assignment.id)},
        message=f"Role '{body.role_name}' assigned successfully.",
    )


@roles_router.get("/me", summary="Get my roles")
async def get_my_roles(
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Return the current user's role assignments."""
    roles = await RoleService.get_user_role_names(
        db, current_user.id, current_user.organization_id
    )
    return success_response(data={"roles": [r.value for r in roles]})
