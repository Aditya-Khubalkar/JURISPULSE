"""
JurisPulse — Agent Registry (Service)
=========================================
22 logical agents registered with their types, capabilities, and required models.

IMPORTANT:
  - Agents are NOT individual AI models
  - Some are DETERMINISTIC (pure backend logic)
  - Some are HYBRID (logic + AI)
  - Some are LLM_BASED (require deployed model)
  - Status reflects actual capability — NOT_DEPLOYED if required model not available
"""

from typing import Dict, List, Optional

from app.core.config.constants import AgentStatus, AgentType

AGENT_DEFINITIONS: List[Dict] = [
    {
        "agent_id": "case_intake_agent",
        "name": "Case Intake Agent",
        "description": "Collects and validates initial case information, creates case record and adds parties.",
        "agent_type": AgentType.DETERMINISTIC.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"creates_case": True, "adds_parties": True, "validates_fields": True},
        "required_models": [],
    },
    {
        "agent_id": "document_processing_agent",
        "name": "Document Processing Agent",
        "description": "Orchestrates the document processing pipeline: validate → OCR → chunk → embed → index.",
        "agent_type": AgentType.HYBRID.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"ocr": True, "chunking": True, "embedding": True},
        "required_models": ["embedding_model"],
    },
    {
        "agent_id": "document_review_agent",
        "name": "Document Review Agent",
        "description": "Reviews document content and flags issues for human attention.",
        "agent_type": AgentType.DETERMINISTIC.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"basic_review": True, "flags_issues": True},
        "required_models": [],
    },
    {
        "agent_id": "metadata_extraction_agent",
        "name": "Metadata Extraction Agent",
        "description": "Extracts metadata from documents (dates, case numbers, parties).",
        "agent_type": AgentType.HYBRID.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"regex_extraction": True, "ner_extraction": False},
        "required_models": [],  # NER model is NOT_DEPLOYED
    },
    {
        "agent_id": "evidence_extraction_agent",
        "name": "Evidence Extraction Agent",
        "description": "Identifies and extracts evidence from documents.",
        "agent_type": AgentType.HYBRID.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"rule_based": True, "ai_extraction": False},
        "required_models": [],
    },
    {
        "agent_id": "legal_research_agent",
        "name": "Legal Research Agent",
        "description": "Runs semantic search over the Indian legal corpus to find relevant precedents.",
        "agent_type": AgentType.HYBRID.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"semantic_search": True, "vector_retrieval": True},
        "required_models": ["embedding_model"],
    },
    {
        "agent_id": "precedent_research_agent",
        "name": "Precedent Research Agent",
        "description": "Finds and ranks relevant case precedents for a legal matter.",
        "agent_type": AgentType.HYBRID.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"precedent_search": True, "ranking": True},
        "required_models": ["embedding_model"],
    },
    {
        "agent_id": "semantic_search_agent",
        "name": "Semantic Search Agent",
        "description": "Low-level agent that executes vector similarity search.",
        "agent_type": AgentType.HYBRID.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"vector_search": True},
        "required_models": ["embedding_model"],
    },
    {
        "agent_id": "citation_verification_agent",
        "name": "Citation Verification Agent",
        "description": "Verifies legal citations against known sources.",
        "agent_type": AgentType.DETERMINISTIC.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"format_validation": True, "source_lookup": False},
        "required_models": [],
    },
    {
        "agent_id": "legal_drafting_agent",
        "name": "Legal Drafting Agent",
        "description": "Generates legal documents using the Llama 3.1 LoRA model.",
        "agent_type": AgentType.LLM_BASED.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {
            "document_types": ["petition", "affidavit", "bail_application", "notice", "appeal"],
            "uses_rag": True,
        },
        "required_models": ["legal_drafter", "embedding_model"],
    },
    {
        "agent_id": "hallucination_detection_agent",
        "name": "Hallucination Detection Agent",
        "description": "Checks AI-generated claims against retrieved evidence.",
        "agent_type": AgentType.NOT_DEPLOYED.value,
        "status": AgentStatus.NOT_DEPLOYED.value,
        "capabilities": {"claim_verification": False},
        "required_models": ["hallucination_detector"],
    },
    {
        "agent_id": "timeline_agent",
        "name": "Timeline Agent",
        "description": "Generates and maintains a case timeline from events and documents.",
        "agent_type": AgentType.DETERMINISTIC.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"event_tracking": True, "ai_extraction": False},
        "required_models": [],
    },
    {
        "agent_id": "hearing_agent",
        "name": "Hearing Agent",
        "description": "Manages hearing scheduling, reminders, and outcome recording.",
        "agent_type": AgentType.DETERMINISTIC.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"scheduling": True, "reminders": True},
        "required_models": [],
    },
    {
        "agent_id": "deadline_agent",
        "name": "Deadline Agent",
        "description": "Tracks legal deadlines and sends reminders.",
        "agent_type": AgentType.DETERMINISTIC.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"deadline_tracking": True, "notifications": True},
        "required_models": [],
    },
    {
        "agent_id": "task_agent",
        "name": "Task Agent",
        "description": "Manages task creation, assignment, and tracking.",
        "agent_type": AgentType.DETERMINISTIC.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"task_management": True},
        "required_models": [],
    },
    {
        "agent_id": "case_summary_agent",
        "name": "Case Summary Agent",
        "description": "Generates concise case summaries from case data.",
        "agent_type": AgentType.LLM_BASED.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"summarization": True},
        "required_models": ["legal_drafter"],
    },
    {
        "agent_id": "contradiction_detection_agent",
        "name": "Contradiction Detection Agent",
        "description": "Identifies logical contradictions in documents and claims.",
        "agent_type": AgentType.NOT_DEPLOYED.value,
        "status": AgentStatus.NOT_DEPLOYED.value,
        "capabilities": {"contradiction_detection": False},
        "required_models": ["hallucination_detector"],
    },
    {
        "agent_id": "risk_analysis_agent",
        "name": "Risk Analysis Agent",
        "description": "Assesses legal risk from case facts and evidence.",
        "agent_type": AgentType.NOT_DEPLOYED.value,
        "status": AgentStatus.NOT_DEPLOYED.value,
        "capabilities": {"risk_scoring": False},
        "required_models": ["risk_assessor"],
    },
    {
        "agent_id": "client_summary_agent",
        "name": "Client Summary Agent",
        "description": "Generates client-friendly summaries of case status.",
        "agent_type": AgentType.LLM_BASED.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"client_report": True},
        "required_models": ["legal_drafter"],
    },
    {
        "agent_id": "notification_agent",
        "name": "Notification Agent",
        "description": "Dispatches in-app and email notifications for events.",
        "agent_type": AgentType.DETERMINISTIC.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"in_app": True, "email": True},
        "required_models": [],
    },
    {
        "agent_id": "audit_agent",
        "name": "Audit Agent",
        "description": "Records and queries audit trail for all system actions.",
        "agent_type": AgentType.DETERMINISTIC.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"audit_logging": True, "audit_query": True},
        "required_models": [],
    },
    {
        "agent_id": "orchestrator_agent",
        "name": "Orchestrator Agent",
        "description": "Coordinates multi-agent workflows and tracks execution state.",
        "agent_type": AgentType.DETERMINISTIC.value,
        "status": AgentStatus.AVAILABLE.value,
        "capabilities": {"workflow_orchestration": True, "state_tracking": True},
        "required_models": [],
    },
]


class AgentRegistryService:
    """In-memory agent registry backed by AGENT_DEFINITIONS."""

    @classmethod
    def get_all(cls) -> List[Dict]:
        return AGENT_DEFINITIONS

    @classmethod
    def get(cls, agent_id: str) -> Optional[Dict]:
        for agent in AGENT_DEFINITIONS:
            if agent["agent_id"] == agent_id:
                return agent
        return None

    @classmethod
    def get_available(cls) -> List[Dict]:
        return [a for a in AGENT_DEFINITIONS if a["status"] == AgentStatus.AVAILABLE.value]
