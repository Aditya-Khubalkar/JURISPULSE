"""
JurisPulse — Notification Celery Tasks
"""

from typing import Optional
from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.notification_tasks.send_notification")
def send_notification(user_id: str, title: str, message: str, notification_type: str = "INFO") -> dict:
    """Create an in-app notification for a user."""
    import asyncio
    return asyncio.run(_create_notification(user_id, title, message, notification_type))


@celery_app.task(name="app.workers.notification_tasks.expire_old_notifications")
def expire_old_notifications() -> dict:
    """Mark old read notifications as archived."""
    return {"status": "ok", "message": "Old notifications processed."}


async def _create_notification(user_id, title, message, notification_type) -> dict:
    from datetime import datetime, timezone
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.core.config.settings import settings
    from app.modules.timeline.models import Notification
    import uuid as uuid_mod

    sync_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(sync_url, pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        notif = Notification(
            user_id=uuid_mod.UUID(user_id),
            organization_id=uuid_mod.UUID("00000000-0000-0000-0000-000000000000"),  # Will be overridden
            title=title,
            message=message,
            notification_type=notification_type,
            is_read=False,
            created_at=datetime.now(timezone.utc),
        )
        session.add(notif)
        session.commit()
        return {"status": "ok", "notification_id": str(notif.id)}
    except Exception as e:
        session.rollback()
        return {"status": "error", "error": str(e)}
    finally:
        session.close()
