"""
JurisPulse — Central API Router (v1)
========================================
All API sub-routers are registered here.
This file is the single source of truth for the URL structure.

All routes are mounted at /api/v1/.

IMPORTANT: When adding a new module, import its router here and
add it to the include list. Do NOT register routers directly in main.py.
"""

from fastapi import APIRouter

# Health (Phase 1)
from app.api.health import health_router

# Auth & Identity (Phase 2)
from app.modules.auth.router import auth_router
from app.modules.users.router import users_router
from app.modules.organizations.router import organizations_router
from app.modules.roles.router import roles_router

# Case Domain (Phase 3)
from app.modules.clients.router import clients_router
from app.modules.cases.router import cases_router

# Documents & Storage (Phase 4)
from app.modules.documents.router import documents_router
from app.modules.documents.local_router import local_router  # dev-only, no auth/DB
from app.modules.evidence.router import evidence_router

# Research & Retrieval (Phase 5)
from app.modules.research.router import research_router

# Drafting (Phase 6)
from app.modules.drafting.router import drafting_router

# Verification & Approvals (Phase 7)
from app.modules.verification.router import verification_router

# Agents & Workflows (Phase 8)
from app.modules.agents.router import agents_router
from app.workflows.router import workflows_router

# Legal workflow domain (Phase 9)
from app.modules.timeline.router import timeline_router
from app.modules.hearings.router import hearings_router
from app.modules.tasks.router import tasks_router
from app.modules.notifications.router import notifications_router
from app.modules.collaboration.router import collaboration_router

# Admin, Analytics, Reports (Phase 10)
from app.modules.admin.router import admin_router
from app.modules.analytics.router import analytics_router
from app.modules.reports.router import reports_router

API_V1_PREFIX = "/api/v1"

api_router = APIRouter(prefix=API_V1_PREFIX)

# ---- System ----
api_router.include_router(health_router, tags=["System"])

# ---- Auth & Identity ----
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(organizations_router, prefix="/organizations", tags=["Organizations"])
api_router.include_router(roles_router, prefix="/roles", tags=["Roles & Permissions"])

# ---- Case Domain ----
api_router.include_router(clients_router, prefix="/clients", tags=["Clients"])
api_router.include_router(cases_router, prefix="/cases", tags=["Cases"])

# ---- Documents ----
api_router.include_router(documents_router, prefix="/documents", tags=["Documents"])
api_router.include_router(local_router, prefix="/local", tags=["Local Storage (Dev)"])  # no auth required
api_router.include_router(evidence_router, prefix="/evidence", tags=["Evidence"])

# ---- Research ----
api_router.include_router(research_router, prefix="/research", tags=["Legal Research"])

# ---- Drafting ----
api_router.include_router(drafting_router, prefix="/drafts", tags=["AI Drafting"])

# ---- Verification ----
api_router.include_router(verification_router, prefix="/verification", tags=["Verification"])

# ---- Agents & Workflows ----
api_router.include_router(agents_router, prefix="/agents", tags=["Agents"])
api_router.include_router(workflows_router, prefix="/workflows", tags=["Workflows"])

# ---- Legal Workflow Domain ----
api_router.include_router(timeline_router, prefix="/timeline", tags=["Case Timeline"])
api_router.include_router(hearings_router, prefix="/hearings", tags=["Hearings"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(collaboration_router, prefix="/collaboration", tags=["Collaboration"])

# ---- Admin & Reporting ----
api_router.include_router(admin_router, prefix="/admin", tags=["Admin"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(reports_router, prefix="/reports", tags=["Reports"])
