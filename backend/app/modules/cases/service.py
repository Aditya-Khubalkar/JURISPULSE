"""
JurisPulse — Cases Service
=============================
Business logic for case management.
Organization isolation is enforced here — not just in routes.
"""

import uuid
from typing import List, Optional, Tuple

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.audit.service import AuditService
from app.modules.cases.models import Case, CaseMember, CaseParty
from app.modules.cases.repository import CaseRepository
from app.modules.cases.schemas import (
    CaseCreate,
    CaseMemberCreate,
    CasePartyCreate,
    CaseUpdate,
)
from app.core.config.constants import AuditAction
from app.utils.exceptions import (
    CaseAccessDeniedError,
    CaseNotFoundError,
    ConflictError,
)

logger = structlog.get_logger("jurispulse.cases.service")


class CaseService:
    """Business logic for the Case domain."""

    @staticmethod
    async def _assert_access(
        db: AsyncSession,
        case_id: uuid.UUID,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        require_member: bool = True,
    ) -> Case:
        """
        Load a case and verify the user has access.
        Raises CaseNotFoundError or CaseAccessDeniedError as appropriate.
        """
        case = await CaseRepository.get_by_id(db, case_id, organization_id)
        if not case:
            raise CaseNotFoundError(str(case_id))

        if require_member:
            member = await CaseRepository.get_member(db, case_id, user_id)
            if not member:
                raise CaseAccessDeniedError()

        return case

    @staticmethod
    async def create_case(
        db: AsyncSession,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        data: CaseCreate,
    ) -> Case:
        """Create a new case and add the creator as lead member."""
        parties = data.parties or []
        case_data = data.model_dump(exclude={"parties"})

        case = await CaseRepository.create(
            db,
            organization_id=organization_id,
            created_by=user_id,
            **case_data,
        )

        # Add creator as lead member
        await CaseRepository.add_member(
            db,
            case_id=case.id,
            user_id=user_id,
            role="LEAD",
            is_lead=True,
            added_by=user_id,
        )

        # Add parties if provided
        for party in parties:
            await CaseRepository.add_party(
                db,
                case_id=case.id,
                **party.model_dump(),
            )

        await AuditService.log(
            db,
            actor_id=user_id,
            organization_id=organization_id,
            action=AuditAction.CASE_CREATE,
            resource="cases",
            resource_id=str(case.id),
        )

        logger.info("case.created", case_id=str(case.id), org_id=str(organization_id))
        return case

    @staticmethod
    async def get_case(
        db: AsyncSession,
        case_id: uuid.UUID,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Case:
        """Get a case with parties and members loaded."""
        case = await CaseRepository.get_by_id(
            db, case_id, organization_id,
            include_parties=True,
            include_members=True,
        )
        if not case:
            raise CaseNotFoundError(str(case_id))

        # Check member access
        member = await CaseRepository.get_member(db, case_id, user_id)
        if not member:
            raise CaseAccessDeniedError()

        return case

    @staticmethod
    async def list_cases(
        db: AsyncSession,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        is_admin: bool = False,
        **filters,
    ) -> Tuple[List[Case], int]:
        """
        List cases accessible to the user.
        Admins see all org cases; others see only cases they're members of.
        """
        user_filter = None if is_admin else user_id
        return await CaseRepository.list_cases(
            db,
            organization_id=organization_id,
            user_id=user_filter,
            **filters,
        )

    @staticmethod
    async def update_case(
        db: AsyncSession,
        case_id: uuid.UUID,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        data: CaseUpdate,
    ) -> Case:
        """Update a case. User must be a member."""
        case = await CaseService._assert_access(db, case_id, organization_id, user_id)
        updates = {k: v for k, v in data.model_dump().items() if v is not None}
        updated = await CaseRepository.update(db, case, **updates)

        await AuditService.log(
            db,
            actor_id=user_id,
            organization_id=organization_id,
            action=AuditAction.CASE_UPDATE,
            resource="cases",
            resource_id=str(case_id),
            metadata={"fields": list(updates.keys())},
        )
        return updated

    @staticmethod
    async def add_member(
        db: AsyncSession,
        case_id: uuid.UUID,
        organization_id: uuid.UUID,
        requesting_user_id: uuid.UUID,
        data: CaseMemberCreate,
    ) -> CaseMember:
        """Add a user to a case. Only lead members can add new members."""
        case = await CaseService._assert_access(
            db, case_id, organization_id, requesting_user_id
        )
        # Check if already a member
        existing = await CaseRepository.get_member(db, case_id, data.user_id)
        if existing:
            raise ConflictError("User is already a member of this case.")

        return await CaseRepository.add_member(
            db,
            case_id=case_id,
            user_id=data.user_id,
            role=data.role.value,
            is_lead=data.is_lead,
            added_by=requesting_user_id,
        )

    @staticmethod
    async def add_party(
        db: AsyncSession,
        case_id: uuid.UUID,
        organization_id: uuid.UUID,
        user_id: uuid.UUID,
        data: CasePartyCreate,
    ) -> CaseParty:
        """Add a party to a case."""
        await CaseService._assert_access(db, case_id, organization_id, user_id)
        return await CaseRepository.add_party(db, case_id=case_id, **data.model_dump())
