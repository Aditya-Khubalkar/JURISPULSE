"""
JurisPulse — Reports Router
Routes: /api/v1/reports/*
"""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser, require_firm_admin
from app.modules.auth.models import User
from app.database.session import get_db
from app.utils.responses import created_response, success_response

reports_router = APIRouter()


class ReportRequest(BaseModel):
    report_type: str  # "case_summary", "activity_log", "research_summary"
    case_id: Optional[uuid.UUID] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None


@reports_router.post("/generate", summary="Queue report generation", status_code=202)
async def generate_report(
    body: ReportRequest,
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_firm_admin()),
):
    """
    Queue a report for generation.
    Reports are generated asynchronously via Celery.
    Returns a job ID to poll for status.
    """
    # Import here to avoid circular import at module load
    from app.workers.report_tasks import generate_report as report_task

    job = report_task.delay(
        report_type=body.report_type,
        organization_id=str(current_user.organization_id),
        case_id=str(body.case_id) if body.case_id else None,
        requested_by=str(current_user.id),
        date_from=body.date_from,
        date_to=body.date_to,
    )
    return created_response(
        data={"job_id": job.id, "status": "QUEUED"},
        message="Report generation queued. Poll /reports/job/{job_id} for status.",
    )


@reports_router.get("/job/{job_id}", summary="Get report job status")
async def get_report_job(
    job_id: str,
    current_user: User = Depends(CurrentUser),
):
    """Get the status of a report generation job."""
    from app.workers.celery_app import celery_app
    from celery.result import AsyncResult

    result = AsyncResult(job_id, app=celery_app)
    return success_response(data={
        "job_id": job_id,
        "status": result.status,
        "result": result.result if result.ready() and not result.failed() else None,
    })
