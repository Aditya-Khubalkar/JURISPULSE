"""
JurisPulse — Cases Router
===========================
Routes: /api/v1/cases/*
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser, require_role
from app.modules.auth.models import User
from app.modules.cases.schemas import (
    CaseCreate,
    CaseMemberCreate,
    CasePartyCreate,
    CaseReadWithDetails,
    CaseUpdate,
    CaseListItem,
)
from app.modules.cases.service import CaseService
from app.core.config.constants import CaseStatus, CaseType, Priority, UserRole
from app.database.session import get_db
from app.utils.pagination import PaginationParams, get_pagination_params
from app.utils.responses import created_response, paginated_response, success_response

cases_router = APIRouter()


@cases_router.post("", summary="Create a new case", status_code=201)
async def create_case(
    body: CaseCreate,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Create a new case. The creator is automatically added as lead."""
    case = await CaseService.create_case(
        db,
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        data=body,
    )
    return created_response(
        data={"id": str(case.id), "title": case.title, "status": case.status},
        message="Case created successfully.",
    )


@cases_router.get("", summary="List cases")
async def list_cases(
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination_params),
    status: Optional[str] = Query(default=None),
    case_type: Optional[str] = Query(default=None),
    priority: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None, max_length=100),
):
    """List cases accessible to the current user."""
    from app.modules.roles.service import RoleService
    roles = await RoleService.get_user_role_names(
        db, current_user.id, current_user.organization_id
    )
    is_admin = (
        UserRole.FIRM_ADMIN in roles
        or UserRole.SUPER_ADMIN in roles
        or current_user.is_superuser
    )
    cases, total = await CaseService.list_cases(
        db,
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        is_admin=is_admin,
        status=status,
        case_type=case_type,
        priority=priority,
        search=search,
        offset=pagination.offset,
        limit=pagination.limit,
    )
    data = [CaseListItem.model_validate(c).model_dump() for c in cases]
    return paginated_response(data, total, pagination.page, pagination.page_size)


@cases_router.get("/{case_id}", summary="Get case details")
async def get_case(
    case_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Get full case details including parties and members."""
    case = await CaseService.get_case(
        db,
        case_id=case_id,
        organization_id=current_user.organization_id,
        user_id=current_user.id,
    )
    return success_response(data=CaseReadWithDetails.model_validate(case).model_dump())


@cases_router.patch("/{case_id}", summary="Update case")
async def update_case(
    case_id: uuid.UUID,
    body: CaseUpdate,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Update a case. User must be a case member."""
    case = await CaseService.update_case(
        db,
        case_id=case_id,
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        data=body,
    )
    return success_response(
        data={"id": str(case.id), "status": case.status},
        message="Case updated.",
    )


@cases_router.post("/{case_id}/members", summary="Add case member", status_code=201)
async def add_case_member(
    case_id: uuid.UUID,
    body: CaseMemberCreate,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Add a firm user as a member of this case."""
    member = await CaseService.add_member(
        db,
        case_id=case_id,
        organization_id=current_user.organization_id,
        requesting_user_id=current_user.id,
        data=body,
    )
    return created_response(
        data={"member_id": str(member.id)},
        message="Member added to case.",
    )


@cases_router.post("/{case_id}/parties", summary="Add case party", status_code=201)
async def add_case_party(
    case_id: uuid.UUID,
    body: CasePartyCreate,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Add a party (petitioner, respondent, etc.) to this case."""
    party = await CaseService.add_party(
        db,
        case_id=case_id,
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        data=body,
    )
    return created_response(
        data={"party_id": str(party.id), "name": party.name},
        message="Party added to case.",
    )
