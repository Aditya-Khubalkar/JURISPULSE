"""
JurisPulse — System-Wide Constants and Enumerations
====================================================
All typed enumerations for the entire platform are defined here.
Import from this module — never hard-code string literals for states.
"""

from enum import Enum


# ---------------------------------------------------------------------------
# Case Domain
# ---------------------------------------------------------------------------

class CaseStatus(str, Enum):
    OPEN = "OPEN"
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class CaseType(str, Enum):
    CIVIL = "CIVIL"
    CRIMINAL = "CRIMINAL"
    CONSTITUTIONAL = "CONSTITUTIONAL"
    FAMILY = "FAMILY"
    LABOUR = "LABOUR"
    TAX = "TAX"
    COMMERCIAL = "COMMERCIAL"
    CONSUMER = "CONSUMER"
    ARBITRATION = "ARBITRATION"
    WRIT = "WRIT"
    REVISION = "REVISION"
    APPEAL = "APPEAL"
    OTHER = "OTHER"


class PartyType(str, Enum):
    PETITIONER = "PETITIONER"
    RESPONDENT = "RESPONDENT"
    APPELLANT = "APPELLANT"
    APPELLEE = "APPELLEE"
    PLAINTIFF = "PLAINTIFF"
    DEFENDANT = "DEFENDANT"
    WITNESS = "WITNESS"
    INTERVENOR = "INTERVENOR"
    AMICUS_CURIAE = "AMICUS_CURIAE"
    OTHER = "OTHER"


class CaseMemberRole(str, Enum):
    LEAD = "LEAD"
    ASSOCIATE = "ASSOCIATE"
    OBSERVER = "OBSERVER"
    CLIENT = "CLIENT"


# ---------------------------------------------------------------------------
# Client Domain
# ---------------------------------------------------------------------------

class ClientType(str, Enum):
    INDIVIDUAL = "INDIVIDUAL"
    CORPORATE = "CORPORATE"
    GOVERNMENT = "GOVERNMENT"
    NGO = "NGO"
    OTHER = "OTHER"


# ---------------------------------------------------------------------------
# Document Domain
# ---------------------------------------------------------------------------

class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    VALIDATING = "VALIDATING"
    STORED = "STORED"
    OCR_PENDING = "OCR_PENDING"
    OCR_PROCESSING = "OCR_PROCESSING"
    OCR_COMPLETE = "OCR_COMPLETE"
    CLEANING = "CLEANING"
    METADATA_EXTRACTION = "METADATA_EXTRACTION"
    CLASSIFYING = "CLASSIFYING"
    CHUNKING = "CHUNKING"
    EMBEDDING = "EMBEDDING"
    INDEXING = "INDEXING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class DocumentType(str, Enum):
    PETITION = "petition"
    AFFIDAVIT = "affidavit"
    BAIL_APPLICATION = "bail_application"
    NOTICE = "notice"
    JUDGMENT = "judgment"
    ORDER = "order"
    WRITTEN_STATEMENT = "written_statement"
    APPEAL = "appeal"
    EVIDENCE = "evidence"
    WRITTEN_ARGUMENTS = "written_arguments"
    PLAINT = "plaint"
    VAKALATNAMA = "vakalatnama"
    POWER_OF_ATTORNEY = "power_of_attorney"
    OTHER = "other"


# ---------------------------------------------------------------------------
# Drafting Domain
# ---------------------------------------------------------------------------

class DraftStatus(str, Enum):
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    FINAL = "FINAL"


class DraftGenerationType(str, Enum):
    AI_GENERATED = "AI_GENERATED"
    MANUAL = "MANUAL"
    HYBRID = "HYBRID"


# ---------------------------------------------------------------------------
# AI / Model Domain
# ---------------------------------------------------------------------------

class ModelStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"
    NOT_DEPLOYED = "NOT_DEPLOYED"
    DISABLED = "DISABLED"


class ModelType(str, Enum):
    LLM = "LLM"
    EMBEDDING = "EMBEDDING"
    CLASSIFIER = "CLASSIFIER"
    NER = "NER"
    RERANKER = "RERANKER"
    SUMMARIZER = "SUMMARIZER"
    HALLUCINATION_DETECTOR = "HALLUCINATION_DETECTOR"
    TRANSLATION = "TRANSLATION"
    RISK_ASSESSMENT = "RISK_ASSESSMENT"
    SIMILARITY = "SIMILARITY"
    OTHER = "OTHER"


# ---------------------------------------------------------------------------
# Verification Domain
# ---------------------------------------------------------------------------

class VerificationStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    UNVERIFIED = "UNVERIFIED"
    NOT_DEPLOYED = "NOT_DEPLOYED"


class ClaimType(str, Enum):
    FACT = "FACT"
    DATE = "DATE"
    PERSON = "PERSON"
    CASE_NAME = "CASE_NAME"
    COURT = "COURT"
    SECTION = "SECTION"
    ARTICLE = "ARTICLE"
    CITATION = "CITATION"
    LEGAL_PROPOSITION = "LEGAL_PROPOSITION"
    STATISTICAL_CLAIM = "STATISTICAL_CLAIM"


class CitationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    INVALID = "INVALID"
    DISPUTED = "DISPUTED"


# ---------------------------------------------------------------------------
# Approval / Human-in-the-Loop
# ---------------------------------------------------------------------------

class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    REJECTED = "REJECTED"


class ApprovalResourceType(str, Enum):
    DRAFT = "DRAFT"
    VERIFICATION = "VERIFICATION"
    DOCUMENT = "DOCUMENT"
    CASE_ACTION = "CASE_ACTION"
    WORKFLOW = "WORKFLOW"


# ---------------------------------------------------------------------------
# Agent Domain
# ---------------------------------------------------------------------------

class AgentStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    RUNNING = "RUNNING"
    DISABLED = "DISABLED"
    ERROR = "ERROR"
    NOT_DEPLOYED = "NOT_DEPLOYED"


class AgentType(str, Enum):
    DETERMINISTIC = "DETERMINISTIC"
    LLM_BASED = "LLM_BASED"
    HYBRID = "HYBRID"
    NOT_DEPLOYED = "NOT_DEPLOYED"


class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"


# ---------------------------------------------------------------------------
# Workflow Domain
# ---------------------------------------------------------------------------

class WorkflowStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class WorkflowType(str, Enum):
    DOCUMENT_PROCESSING = "DOCUMENT_PROCESSING"
    LEGAL_RESEARCH = "LEGAL_RESEARCH"
    DRAFT_GENERATION = "DRAFT_GENERATION"
    VERIFICATION = "VERIFICATION"
    CASE_INTAKE = "CASE_INTAKE"
    EVIDENCE_ANALYSIS = "EVIDENCE_ANALYSIS"
    FULL_PIPELINE = "FULL_PIPELINE"


# ---------------------------------------------------------------------------
# Timeline Domain
# ---------------------------------------------------------------------------

class TimelineEventType(str, Enum):
    FILING = "filing"
    NOTICE = "notice"
    REPLY = "reply"
    EVIDENCE = "evidence"
    HEARING = "hearing"
    ORDER = "order"
    JUDGMENT = "judgment"
    DEADLINE = "deadline"
    APPEAL = "appeal"
    SETTLEMENT = "settlement"
    CUSTOM = "custom"


# ---------------------------------------------------------------------------
# Hearings Domain
# ---------------------------------------------------------------------------

class HearingStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    ADJOURNED = "ADJOURNED"
    CANCELLED = "CANCELLED"
    PENDING_NOTICE = "PENDING_NOTICE"


class HearingPurpose(str, Enum):
    FIRST_HEARING = "FIRST_HEARING"
    ARGUMENTS = "ARGUMENTS"
    EVIDENCE = "EVIDENCE"
    FINAL_HEARING = "FINAL_HEARING"
    BAIL = "BAIL"
    INTERIM_RELIEF = "INTERIM_RELIEF"
    MENTIONING = "MENTIONING"
    OTHER = "OTHER"


# ---------------------------------------------------------------------------
# Task Domain
# ---------------------------------------------------------------------------

class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"
    BLOCKED = "BLOCKED"


# ---------------------------------------------------------------------------
# Notification Domain
# ---------------------------------------------------------------------------

class NotificationType(str, Enum):
    HEARING_REMINDER = "HEARING_REMINDER"
    DEADLINE = "DEADLINE"
    DOCUMENT_READY = "DOCUMENT_READY"
    DRAFT_READY = "DRAFT_READY"
    VERIFICATION_ALERT = "VERIFICATION_ALERT"
    TASK_ASSIGNED = "TASK_ASSIGNED"
    COMMENT = "COMMENT"
    CASE_UPDATE = "CASE_UPDATE"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    APPROVAL_RESOLVED = "APPROVAL_RESOLVED"
    SYSTEM = "SYSTEM"


# ---------------------------------------------------------------------------
# RBAC / User Domain
# ---------------------------------------------------------------------------

class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    FIRM_ADMIN = "FIRM_ADMIN"
    SENIOR_LAWYER = "SENIOR_LAWYER"
    JUNIOR_LAWYER = "JUNIOR_LAWYER"
    PARALEGAL = "PARALEGAL"
    RESEARCHER = "RESEARCHER"
    CLIENT = "CLIENT"
    GUEST = "GUEST"


class PermissionAction(str, Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    MANAGE = "MANAGE"
    APPROVE = "APPROVE"
    EXPORT = "EXPORT"


class PermissionResource(str, Enum):
    CASES = "CASES"
    DOCUMENTS = "DOCUMENTS"
    DRAFTS = "DRAFTS"
    RESEARCH = "RESEARCH"
    CLIENTS = "CLIENTS"
    USERS = "USERS"
    ROLES = "ROLES"
    MODELS = "MODELS"
    WORKFLOWS = "WORKFLOWS"
    ANALYTICS = "ANALYTICS"
    AUDIT_LOGS = "AUDIT_LOGS"
    APPROVALS = "APPROVALS"
    HEARINGS = "HEARINGS"
    TASKS = "TASKS"
    NOTIFICATIONS = "NOTIFICATIONS"
    ADMIN = "ADMIN"


# ---------------------------------------------------------------------------
# Storage Domain
# ---------------------------------------------------------------------------

class StorageProvider(str, Enum):
    SUPABASE = "SUPABASE"
    LOCAL = "LOCAL"
    MINIO = "MINIO"
    S3 = "S3"


# ---------------------------------------------------------------------------
# Dataset Domain
# ---------------------------------------------------------------------------

class DatasetStatus(str, Enum):
    READY = "READY"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"
    OUTDATED = "OUTDATED"


class DatasetType(str, Enum):
    LEGAL_CORPUS = "LEGAL_CORPUS"
    CASE_LAW = "CASE_LAW"
    STATUTES = "STATUTES"
    HALLUCINATION_TRAINING = "HALLUCINATION_TRAINING"
    NER_TRAINING = "NER_TRAINING"
    CLASSIFICATION_TRAINING = "CLASSIFICATION_TRAINING"
    OTHER = "OTHER"


# ---------------------------------------------------------------------------
# Audit Domain
# ---------------------------------------------------------------------------

class AuditAction(str, Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    REGISTER = "REGISTER"
    PASSWORD_RESET = "PASSWORD_RESET"
    CASE_CREATE = "CASE_CREATE"
    CASE_UPDATE = "CASE_UPDATE"
    CASE_DELETE = "CASE_DELETE"
    CASE_ARCHIVE = "CASE_ARCHIVE"
    DOCUMENT_UPLOAD = "DOCUMENT_UPLOAD"
    DOCUMENT_DELETE = "DOCUMENT_DELETE"
    DOCUMENT_DOWNLOAD = "DOCUMENT_DOWNLOAD"
    RESEARCH_REQUEST = "RESEARCH_REQUEST"
    DRAFT_GENERATE = "DRAFT_GENERATE"
    DRAFT_UPDATE = "DRAFT_UPDATE"
    DRAFT_DELETE = "DRAFT_DELETE"
    VERIFICATION_REQUEST = "VERIFICATION_REQUEST"
    APPROVAL_CREATE = "APPROVAL_CREATE"
    APPROVAL_RESOLVE = "APPROVAL_RESOLVE"
    ROLE_ASSIGN = "ROLE_ASSIGN"
    ROLE_REVOKE = "ROLE_REVOKE"
    PERMISSION_CHANGE = "PERMISSION_CHANGE"
    USER_CREATE = "USER_CREATE"
    USER_UPDATE = "USER_UPDATE"
    USER_DELETE = "USER_DELETE"
    USER_DEACTIVATE = "USER_DEACTIVATE"
    ADMIN_ACTION = "ADMIN_ACTION"
    DATA_EXPORT = "DATA_EXPORT"
    WORKFLOW_START = "WORKFLOW_START"
    WORKFLOW_CANCEL = "WORKFLOW_CANCEL"
    CLIENT_CREATE = "CLIENT_CREATE"
    CLIENT_UPDATE = "CLIENT_UPDATE"


# ---------------------------------------------------------------------------
# Research Domain
# ---------------------------------------------------------------------------

class ResearchQueryStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# ---------------------------------------------------------------------------
# OCR Domain
# ---------------------------------------------------------------------------

class OCRStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


# ---------------------------------------------------------------------------
# System-level
# ---------------------------------------------------------------------------

# Supported Indian courts — for reference in UI / validation
INDIAN_COURTS = [
    "Supreme Court of India",
    "High Court of Delhi",
    "High Court of Bombay",
    "High Court of Calcutta",
    "High Court of Madras",
    "High Court of Allahabad",
    "High Court of Karnataka",
    "High Court of Gujarat",
    "High Court of Rajasthan",
    "High Court of Punjab & Haryana",
    "High Court of Andhra Pradesh",
    "High Court of Telangana",
    "High Court of Kerala",
    "High Court of Gauhati",
    "High Court of Chhattisgarh",
    "High Court of Jharkhand",
    "High Court of Uttarakhand",
    "High Court of Himachal Pradesh",
    "High Court of Jammu & Kashmir",
    "High Court of Manipur",
    "High Court of Meghalaya",
    "High Court of Orissa",
    "High Court of Patna",
    "High Court of Sikkim",
    "High Court of Tripura",
    "District Court",
    "Sessions Court",
    "Magistrate Court",
    "Family Court",
    "Consumer Forum",
    "Debt Recovery Tribunal",
    "National Company Law Tribunal",
    "Income Tax Appellate Tribunal",
    "Central Administrative Tribunal",
    "Armed Forces Tribunal",
    "Other",
]

# Supported jurisdictions
INDIAN_JURISDICTIONS = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "Delhi",
    "Jammu & Kashmir",
    "Ladakh",
    "Chandigarh",
    "Puducherry",
    "Pan India",
]

# File upload constraints
MAX_FILE_SIZE_BYTES = 52_428_800  # 50 MB
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".tif", ".doc", ".docx", ".txt"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/tiff",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}

# API version prefix
API_V1_PREFIX = "/api/v1"

# Pagination defaults
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
