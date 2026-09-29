"""
JurisPulse — Analytics Router
Routes: /api/v1/analytics/*
"""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.dependencies import CurrentUser, require_firm_admin
from app.modules.auth.models import User
from app.modules.cases.models import Case
from app.database.session import get_db
from app.modules.documents.models import Document
from app.modules.drafting.models import Draft
from app.modules.research.models import ResearchQuery
from app.utils.responses import success_response

analytics_router = APIRouter()


@analytics_router.get("/dashboard", summary="Dashboard analytics")
async def get_dashboard(
    current_user: User = Depends(CurrentUser),
    db: AsyncSession = Depends(get_db),
    _: None = Depends(require_firm_admin()),
):
    """Return high-level dashboard statistics for the organization."""
    org_id = current_user.organization_id

    cases_total = await db.execute(
        select(func.count(Case.id)).where(Case.organization_id == org_id)
    )
    docs_total = await db.execute(
        select(func.count(Document.id)).where(Document.organization_id == org_id)
    )
    drafts_total = await db.execute(
        select(func.count(Draft.id)).where(Draft.organization_id == org_id)
    )
    research_total = await db.execute(
        select(func.count(ResearchQuery.id)).where(ResearchQuery.organization_id == org_id)
    )

    cases_by_status = await db.execute(
        select(Case.status, func.count(Case.id).label("count"))
        .where(Case.organization_id == org_id)
        .group_by(Case.status)
    )

    return success_response(data={
        "cases": {
            "total": cases_total.scalar_one(),
            "by_status": {row.status: row.count for row in cases_by_status.fetchall()},
        },
        "documents": {"total": docs_total.scalar_one()},
        "drafts": {"total": drafts_total.scalar_one()},
        "research_queries": {"total": research_total.scalar_one()},
    })
