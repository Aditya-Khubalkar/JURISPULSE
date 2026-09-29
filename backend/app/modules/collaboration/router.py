"""
JurisPulse — Collaboration Router
Routes: /api/v1/collaboration/*
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.database.session import get_db
from app.modules.timeline.models import Comment
from app.utils.responses import created_response, success_response

collaboration_router = APIRouter()


class CommentCreate(BaseModel):
    case_id: uuid.UUID
    content: str = Field(min_length=1, max_length=5000)
    is_internal: bool = True
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    parent_comment_id: Optional[uuid.UUID] = None


@collaboration_router.post("/comments", summary="Post comment", status_code=201)
async def post_comment(
    body: CommentCreate,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    comment = Comment(
        organization_id=current_user.organization_id,
        case_id=body.case_id,
        author_id=current_user.id,
        content=body.content,
        is_internal=body.is_internal,
        parent_comment_id=body.parent_comment_id,
        resource_type=body.resource_type,
        resource_id=body.resource_id,
    )
    db.add(comment)
    await db.flush()
    await db.refresh(comment)
    return created_response(data={"id": str(comment.id), "is_internal": comment.is_internal})


@collaboration_router.get("/comments/{case_id}", summary="Get case comments")
async def get_comments(
    case_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
    include_client_visible: bool = False,
):
    query = select(Comment).where(
        Comment.case_id == case_id,
        Comment.organization_id == current_user.organization_id,
        Comment.is_deleted == False,
    )
    if not include_client_visible:
        query = query.where(Comment.is_internal == True)
    result = await db.execute(query.order_by(Comment.created_at))
    comments = result.scalars().all()
    return success_response(data=[
        {
            "id": str(c.id),
            "content": c.content,
            "author_id": str(c.author_id),
            "is_internal": c.is_internal,
            "parent_comment_id": str(c.parent_comment_id) if c.parent_comment_id else None,
            "created_at": c.created_at.isoformat(),
        }
        for c in comments
    ])
