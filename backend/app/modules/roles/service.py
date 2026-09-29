"""
JurisPulse — Role Service
===========================
Business logic for role and permission management.
"""

import uuid
from typing import List, Optional, Set

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.config.constants import UserRole as UserRoleEnum
from app.modules.roles.models import Permission, Role, RolePermission, UserRole

logger = structlog.get_logger("jurispulse.roles.service")


class RoleService:
    """Handles role queries and RBAC checks."""

    @staticmethod
    async def get_user_role_names(
        db: AsyncSession,
        user_id: uuid.UUID,
        organization_id: Optional[uuid.UUID] = None,
    ) -> Set[UserRoleEnum]:
        """
        Return the set of role names assigned to a user.
        If organization_id is provided, only returns roles for that org.
        """
        query = (
            select(Role.name)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
        )
        if organization_id:
            query = query.where(UserRole.organization_id == organization_id)

        result = await db.execute(query)
        role_names = result.scalars().all()

        valid_roles: Set[UserRoleEnum] = set()
        for name in role_names:
            try:
                valid_roles.add(UserRoleEnum(name))
            except ValueError:
                logger.warning("roles.unknown_role", role_name=name)
        return valid_roles

    @staticmethod
    async def user_has_permission(
        db: AsyncSession,
        user_id: uuid.UUID,
        resource: str,
        action: str,
        organization_id: Optional[uuid.UUID] = None,
    ) -> bool:
        """
        Check whether a user has a specific resource+action permission
        through any of their assigned roles.
        """
        query = (
            select(Permission.id)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(Role, Role.id == RolePermission.role_id)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(
                UserRole.user_id == user_id,
                Permission.resource == resource,
                Permission.action == action,
            )
        )
        if organization_id:
            query = query.where(UserRole.organization_id == organization_id)

        result = await db.execute(query.limit(1))
        return result.scalar_one_or_none() is not None

    @staticmethod
    async def assign_role(
        db: AsyncSession,
        user_id: uuid.UUID,
        role_name: str,
        organization_id: Optional[uuid.UUID],
        assigned_by: Optional[uuid.UUID] = None,
    ) -> UserRole:
        """Assign a role to a user, creating it if not already assigned."""
        # Find role
        role_result = await db.execute(select(Role).where(Role.name == role_name))
        role = role_result.scalar_one_or_none()
        if not role:
            raise ValueError(f"Role '{role_name}' does not exist.")

        # Check if already assigned
        existing = await db.execute(
            select(UserRole).where(
                UserRole.user_id == user_id,
                UserRole.role_id == role.id,
                UserRole.organization_id == organization_id,
            )
        )
        if existing.scalar_one_or_none():
            raise ValueError("Role is already assigned to this user.")

        assignment = UserRole(
            user_id=user_id,
            role_id=role.id,
            organization_id=organization_id,
            assigned_by=assigned_by,
        )
        db.add(assignment)
        await db.flush()
        return assignment

    @staticmethod
    async def list_all_roles(db: AsyncSession) -> List[Role]:
        """Return all available roles."""
        result = await db.execute(select(Role).order_by(Role.name))
        return list(result.scalars().all())

    @staticmethod
    async def list_permissions(db: AsyncSession) -> List[Permission]:
        """Return all available permissions."""
        result = await db.execute(select(Permission).order_by(Permission.resource, Permission.action))
        return list(result.scalars().all())
