"""
JurisPulse — Clients Router
==============================
Routes: /api/v1/clients/*
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.modules.clients.models import Client
from app.core.config.constants import ClientType
from app.database.session import get_db
from app.utils.exceptions import ForbiddenError, NotFoundError
from app.utils.pagination import PaginationParams, get_pagination_params
from app.utils.responses import created_response, paginated_response, success_response

clients_router = APIRouter()


class ClientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = None
    client_type: ClientType = ClientType.INDIVIDUAL
    company_name: Optional[str] = None
    notes: Optional[str] = None


class ClientRead(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    name: str
    email: Optional[str]
    phone: Optional[str]
    client_type: str
    company_name: Optional[str]
    is_active: bool


@clients_router.post("", summary="Create client", status_code=201)
async def create_client(
    body: ClientCreate,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Create a new client in the current organization."""
    if not current_user.organization_id:
        raise ForbiddenError("No organization context.")

    client = Client(
        organization_id=current_user.organization_id,
        created_by=current_user.id,
        **body.model_dump(),
    )
    db.add(client)
    await db.flush()
    await db.refresh(client)
    return created_response(
        data=ClientRead.model_validate(client).model_dump(),
        message="Client created.",
    )


@clients_router.get("", summary="List clients")
async def list_clients(
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination_params),
    search: Optional[str] = Query(default=None, max_length=100),
):
    """List all clients in the current organization."""
    query = select(Client).where(
        Client.organization_id == current_user.organization_id,
        Client.is_active == True,
    )
    if search:
        query = query.where(
            Client.name.ilike(f"%{search}%")
        )
    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar_one()
    result = await db.execute(
        query.order_by(Client.name).offset(pagination.offset).limit(pagination.limit)
    )
    clients = result.scalars().all()
    return paginated_response(
        [ClientRead.model_validate(c).model_dump() for c in clients],
        total, pagination.page, pagination.page_size,
    )


@clients_router.get("/{client_id}", summary="Get client by ID")
async def get_client(
    client_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    """Get a client by ID (org-scoped)."""
    result = await db.execute(
        select(Client).where(
            Client.id == client_id,
            Client.organization_id == current_user.organization_id,
        )
    )
    client = result.scalar_one_or_none()
    if not client:
        raise NotFoundError("Client", str(client_id))
    return success_response(data=ClientRead.model_validate(client).model_dump())
