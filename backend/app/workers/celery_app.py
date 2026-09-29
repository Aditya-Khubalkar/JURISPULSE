"""
JurisPulse — Celery Application
===================================
Initialises the Celery app with Redis as broker and result backend.
All task queues are defined here.

Queue routing:
  default       — general purpose tasks
  documents     — OCR, processing, classification, chunking
  embeddings    — embedding generation and indexing
  notifications — email/in-app notification dispatch
  reports       — large report generation

Workers are started separately from the FastAPI server.
They share the same app code but run in separate processes.
"""

from celery import Celery
from celery.schedules import crontab

from app.core.config.settings import settings


def create_celery_app() -> Celery:
    """Create and configure the Celery application."""
    app = Celery(
        "jurispulse",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
        include=[
            "app.workers.document_tasks",
            "app.workers.embedding_tasks",
            "app.workers.report_tasks",
            "app.workers.notification_tasks",
        ],
    )

    app.conf.update(
        # Serialization
        task_serializer=settings.CELERY_TASK_SERIALIZER,
        result_serializer=settings.CELERY_RESULT_SERIALIZER,
        accept_content=["json"],
        # Timezone
        timezone=settings.CELERY_TIMEZONE,
        enable_utc=True,
        # Reliability
        task_track_started=settings.CELERY_TASK_TRACK_STARTED,
        task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
        task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT,
        task_acks_late=True,
        task_reject_on_worker_lost=True,
        # Result expiry
        result_expires=86400,  # 24 hours
        # Queue routing
        task_routes={
            "app.workers.document_tasks.*": {"queue": "documents"},
            "app.workers.embedding_tasks.*": {"queue": "embeddings"},
            "app.workers.notification_tasks.*": {"queue": "notifications"},
            "app.workers.report_tasks.*": {"queue": "reports"},
        },
        # Beat schedule (recurring tasks)
        beat_schedule={
            "ai-gateway-health-check": {
                "task": "app.workers.document_tasks.check_ai_gateway_health",
                "schedule": settings.AI_HEALTH_CHECK_INTERVAL,
                "options": {"queue": "default"},
            },
            "expire-old-notifications": {
                "task": "app.workers.notification_tasks.expire_old_notifications",
                "schedule": crontab(hour="2", minute="0"),  # daily at 2am
                "options": {"queue": "notifications"},
            },
        },
    )

    return app


celery_app: Celery = create_celery_app()
