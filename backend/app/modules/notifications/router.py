"""
JurisPulse — Notifications Router
Routes: /api/v1/notifications/*
"""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser
from app.modules.auth.models import User
from app.database.session import get_db
from app.modules.timeline.models import Notification
from app.utils.responses import success_response

notifications_router = APIRouter()


@notifications_router.get("", summary="Get my notifications")
async def get_notifications(
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
    unread_only: bool = False,
):
    query = select(Notification).where(Notification.user_id == current_user.id)
    if unread_only:
        query = query.where(Notification.is_read == False)
    result = await db.execute(
        query.order_by(Notification.created_at.desc()).limit(50)
    )
    notifications = result.scalars().all()
    return success_response(data=[
        {
            "id": str(n.id),
            "title": n.title,
            "message": n.message,
            "type": n.notification_type,
            "is_read": n.is_read,
            "resource_type": n.resource_type,
            "resource_id": n.resource_id,
            "created_at": n.created_at.isoformat(),
        }
        for n in notifications
    ])


@notifications_router.post("/{notification_id}/read", summary="Mark notification as read")
async def mark_read(
    notification_id: uuid.UUID,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
):
    from datetime import datetime, timezone
    await db.execute(
        update(Notification)
        .where(
            Notification.id == notification_id,
            Notification.user_id == current_user.id,
        )
        .values(is_read=True, read_at=datetime.now(timezone.utc))
    )
    return success_response(message="Notification marked as read.")
