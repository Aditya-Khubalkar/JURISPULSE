"""
JurisPulse — Case Schemas (Pydantic v2)
==========================================
"""

import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator

from app.core.config.constants import (
    CaseMemberRole,
    CaseStatus,
    CaseType,
    PartyType,
    Priority,
)


# ---------------------------------------------------------------------------
# Party schemas
# ---------------------------------------------------------------------------

class CasePartyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    party_type: PartyType = PartyType.PETITIONER
    role: Optional[str] = None
    advocate_name: Optional[str] = None
    contact_information: Optional[Dict[str, Any]] = None


class CasePartyRead(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    name: str
    party_type: str
    role: Optional[str]
    advocate_name: Optional[str]


# ---------------------------------------------------------------------------
# Member schemas
# ---------------------------------------------------------------------------

class CaseMemberCreate(BaseModel):
    user_id: uuid.UUID
    role: CaseMemberRole = CaseMemberRole.ASSOCIATE
    is_lead: bool = False


class CaseMemberRead(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    user_id: uuid.UUID
    role: str
    is_lead: bool


# ---------------------------------------------------------------------------
# Case schemas
# ---------------------------------------------------------------------------

class CaseCreate(BaseModel):
    title: str = Field(min_length=5, max_length=500)
    case_number: Optional[str] = Field(default=None, max_length=100)
    case_type: CaseType = CaseType.CIVIL
    court: Optional[str] = Field(default=None, max_length=255)
    jurisdiction: Optional[str] = Field(default=None, max_length=100)
    filing_date: Optional[date] = None
    priority: Priority = Priority.MEDIUM
    description: Optional[str] = None
    client_id: Optional[uuid.UUID] = None
    is_confidential: bool = False
    metadata: Optional[Dict[str, Any]] = None
    parties: Optional[List[CasePartyCreate]] = None


class CaseUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=5, max_length=500)
    case_number: Optional[str] = Field(default=None, max_length=100)
    case_type: Optional[CaseType] = None
    court: Optional[str] = None
    jurisdiction: Optional[str] = None
    filing_date: Optional[date] = None
    status: Optional[CaseStatus] = None
    priority: Optional[Priority] = None
    description: Optional[str] = None
    is_confidential: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None


class CaseRead(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    organization_id: uuid.UUID
    case_number: Optional[str]
    title: str
    case_type: str
    court: Optional[str]
    jurisdiction: Optional[str]
    filing_date: Optional[date]
    status: str
    priority: str
    description: Optional[str]
    is_confidential: bool
    client_id: Optional[uuid.UUID]
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime


class CaseReadWithDetails(CaseRead):
    parties: List[CasePartyRead] = []
    members: List[CaseMemberRead] = []


class CaseListItem(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    case_number: Optional[str]
    title: str
    case_type: str
    court: Optional[str]
    status: str
    priority: str
    client_id: Optional[uuid.UUID]
    filing_date: Optional[date]
    created_at: datetime
