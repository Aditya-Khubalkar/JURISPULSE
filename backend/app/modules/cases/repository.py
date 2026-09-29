"""
JurisPulse — Cases Repository
================================
Data access layer for the Case domain.
All queries enforce organization isolation.
"""

import uuid
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.modules.cases.models import Case, CaseMember, CaseParty
from app.core.config.constants import CaseStatus


class CaseRepository:
    """Database queries for the Case entity."""

    @staticmethod
    async def create(
        db: AsyncSession,
        organization_id: uuid.UUID,
        created_by: uuid.UUID,
        **kwargs,
    ) -> Case:
        """Create a new case within the organisation."""
        case = Case(
            organization_id=organization_id,
            created_by=created_by,
            **kwargs,
        )
        db.add(case)
        await db.flush()
        await db.refresh(case)
        return case

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        case_id: uuid.UUID,
        organization_id: uuid.UUID,
        include_parties: bool = False,
        include_members: bool = False,
    ) -> Optional[Case]:
        """Get a single case by ID, scoped to the organization."""
        query = select(Case).where(
            Case.id == case_id,
            Case.organization_id == organization_id,
        )
        if include_parties:
            query = query.options(joinedload(Case.parties))
        if include_members:
            query = query.options(joinedload(Case.members))

        result = await db.execute(query)
        return result.unique().scalar_one_or_none()

    @staticmethod
    async def list_cases(
        db: AsyncSession,
        organization_id: uuid.UUID,
        user_id: Optional[uuid.UUID] = None,  # If set, filter to cases user is member of
        status: Optional[str] = None,
        case_type: Optional[str] = None,
        priority: Optional[str] = None,
        client_id: Optional[uuid.UUID] = None,
        search: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> Tuple[List[Case], int]:
        """List cases with optional filters and pagination."""
        query = select(Case).where(Case.organization_id == organization_id)

        if user_id:
            member_subq = select(CaseMember.case_id).where(CaseMember.user_id == user_id)
            query = query.where(Case.id.in_(member_subq))
        if status:
            query = query.where(Case.status == status)
        if case_type:
            query = query.where(Case.case_type == case_type)
        if priority:
            query = query.where(Case.priority == priority)
        if client_id:
            query = query.where(Case.client_id == client_id)
        if search:
            pattern = f"%{search}%"
            query = query.where(
                or_(
                    Case.title.ilike(pattern),
                    Case.case_number.ilike(pattern),
                    Case.court.ilike(pattern),
                )
            )

        total_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = total_result.scalar_one()

        result = await db.execute(
            query.order_by(Case.created_at.desc()).offset(offset).limit(limit)
        )
        return list(result.scalars().all()), total

    @staticmethod
    async def update(
        db: AsyncSession,
        case: Case,
        **updates,
    ) -> Case:
        """Apply updates to a case model instance."""
        for key, value in updates.items():
            if value is not None:
                setattr(case, key, value)
        await db.flush()
        await db.refresh(case)
        return case

    @staticmethod
    async def soft_archive(db: AsyncSession, case: Case) -> Case:
        """Archive a case rather than deleting it."""
        case.status = CaseStatus.ARCHIVED.value
        await db.flush()
        return case

    @staticmethod
    async def add_party(
        db: AsyncSession,
        case_id: uuid.UUID,
        **kwargs,
    ) -> CaseParty:
        party = CaseParty(case_id=case_id, **kwargs)
        db.add(party)
        await db.flush()
        return party

    @staticmethod
    async def add_member(
        db: AsyncSession,
        case_id: uuid.UUID,
        user_id: uuid.UUID,
        role: str,
        is_lead: bool,
        added_by: Optional[uuid.UUID],
    ) -> CaseMember:
        member = CaseMember(
            case_id=case_id,
            user_id=user_id,
            role=role,
            is_lead=is_lead,
            added_by=added_by,
            added_at=datetime.now(timezone.utc),
        )
        db.add(member)
        await db.flush()
        return member

    @staticmethod
    async def get_member(
        db: AsyncSession,
        case_id: uuid.UUID,
        user_id: uuid.UUID,
    ) -> Optional[CaseMember]:
        result = await db.execute(
            select(CaseMember).where(
                CaseMember.case_id == case_id,
                CaseMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()
