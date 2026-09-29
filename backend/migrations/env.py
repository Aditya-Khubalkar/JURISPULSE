"""
Alembic migration environment — async SQLAlchemy configuration.

This file:
1. Loads the database URL from app settings (not from alembic.ini)
2. Imports all SQLAlchemy models so Alembic can detect schema changes
3. Runs migrations in async mode using asyncpg

To generate a new migration:
    cd backend && alembic revision --autogenerate -m "description"

To apply migrations:
    cd backend && alembic upgrade head

To downgrade:
    cd backend && alembic downgrade -1
"""

import sys
import asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# ---------------------------------------------------------------------------
# Load application settings and database URL
# ---------------------------------------------------------------------------
from app.core.config.settings import settings

# ---------------------------------------------------------------------------
# Import ALL models here so Alembic autogenerate can detect them.
# Every model module must be imported — even if unused below.
# ---------------------------------------------------------------------------
from app.database.base import Base  # noqa: F401

# Auth & Identity
from app.modules.auth.models import User, RefreshToken  # noqa: F401
from app.modules.organizations.models import Organization  # noqa: F401
from app.modules.roles.models import Role, Permission, RolePermission, UserRole  # noqa: F401

# Case Domain
from app.modules.clients.models import Client  # noqa: F401
from app.modules.cases.models import Case, CaseParty, CaseMember  # noqa: F401

# Documents
from app.modules.documents.models import Document, DocumentVersion, DocumentMetadata  # noqa: F401
from app.modules.evidence.models import Evidence  # noqa: F401

# Legal Research
from app.modules.research.models import ResearchQuery, ResearchResult  # noqa: F401

# Drafting
from app.modules.drafting.models import Draft, DraftVersion  # noqa: F401

# Verification
from app.modules.verification.models import Citation, VerificationClaim, VerificationResult  # noqa: F401

# Approvals
from app.modules.verification.models import Approval  # noqa: F401

# Agents & Workflows
from app.modules.agents.models import AgentDefinition, AgentExecution  # noqa: F401
from app.workflows.models import WorkflowRun, WorkflowState  # noqa: F401

# AI Model Registry
from app.services.ai.models import AIModelRegistry  # noqa: F401

# Legal Workflow Domain
from app.modules.timeline.models import TimelineEvent  # noqa: F401
from app.modules.hearings.models import Hearing  # noqa: F401
from app.modules.tasks.models import Task  # noqa: F401
from app.modules.notifications.models import Notification  # noqa: F401
from app.modules.collaboration.models import Comment, CaseMention  # noqa: F401

# Admin & Audit
from app.modules.audit.models import AuditLog  # noqa: F401
from app.modules.admin.models import Dataset  # noqa: F401

# ---------------------------------------------------------------------------
# Alembic config & target metadata
# ---------------------------------------------------------------------------
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Override the sqlalchemy.url from the config file with our settings value
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


# ---------------------------------------------------------------------------
# Migration run functions
# ---------------------------------------------------------------------------

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    Generates SQL without connecting to the database — useful for review.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations using an async engine (asyncpg)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (connected to actual DB)."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
