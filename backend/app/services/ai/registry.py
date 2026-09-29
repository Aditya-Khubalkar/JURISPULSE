"""
JurisPulse — AI Model Registry (Service)
==========================================
In-memory + database model registry.
Business services use this to discover model endpoints and capabilities.

CRITICAL: The registry reflects the TRUE state of models:
  - legal_drafter:         AVAILABLE (model trained, service running)
  - embedding_model:       AVAILABLE (bge-small, service running)
  - hallucination_detector: NOT_DEPLOYED (model not yet trained)
  - All future models:     NOT_DEPLOYED

Models are not marked AVAILABLE unless their health check passes.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

import structlog

from app.core.config.constants import ModelStatus, ModelType
from app.core.config.settings import settings

logger = structlog.get_logger("jurispulse.ai_gateway.registry")


@dataclass
class ModelInfo:
    """In-memory representation of a registered AI model."""

    model_id: str
    name: str
    model_type: ModelType
    purpose: str
    endpoint: Optional[str]
    status: ModelStatus
    is_enabled: bool
    timeout_seconds: int = 120
    version: Optional[str] = None
    capabilities: Dict = field(default_factory=dict)
    notes: Optional[str] = None
    last_health_check: Optional[datetime] = None
    last_latency_ms: Optional[float] = None


class AIModelRegistryService:
    """
    In-memory model registry.
    Populated at startup from the CURRENT TRUE state.

    Future models are registered as NOT_DEPLOYED.
    Do NOT set a model to AVAILABLE unless it is actually reachable.
    """

    _models: Dict[str, ModelInfo] = {}

    @classmethod
    def initialize(cls) -> None:
        """
        Register all known models.
        Called once at application startup.
        """
        cls._models = {}

        # ---------------------------------------------------------------
        # MODEL 1: Legal Drafter (Llama 3.1 LoRA) — DONE
        # ---------------------------------------------------------------
        cls._register(ModelInfo(
            model_id="legal_drafter",
            name="Llama 3.1 Legal Drafter (LoRA)",
            model_type=ModelType.LLM,
            purpose=(
                "Generates legal drafts including petitions, affidavits, bail applications, "
                "notices, replies, appeals, written statements, and other Indian legal documents."
            ),
            endpoint=settings.AI_DRAFTER_URL,
            status=ModelStatus.OFFLINE,  # Will be updated by health check
            is_enabled=True,
            timeout_seconds=settings.AI_SERVICE_TIMEOUT,
            version="1.0.0",
            capabilities={
                "document_types": [
                    "petition", "affidavit", "bail_application", "notice",
                    "written_statement", "appeal", "reply", "legal_notice"
                ],
                "supports_case_context": True,
                "supports_sources": True,
                "max_output_tokens": 4096,
            },
        ))

        # ---------------------------------------------------------------
        # MODEL 2: bge-small Embedding Model — DONE (pretrained, not fine-tuned)
        # ---------------------------------------------------------------
        cls._register(ModelInfo(
            model_id="embedding_model",
            name="bge-small-en-v1.5 Embedding Model",
            model_type=ModelType.EMBEDDING,
            purpose=(
                "Generates dense vector embeddings for semantic search and retrieval "
                "from the Indian legal corpus (~14,544 indexed chunks)."
            ),
            endpoint=settings.AI_EMBEDDING_URL,
            status=ModelStatus.OFFLINE,  # Will be updated by health check
            is_enabled=True,
            timeout_seconds=60,
            version="bge-small-en-v1.5",
            capabilities={
                "embedding_dimension": 384,
                "batch_size": 64,
                "max_input_tokens": 512,
                "normalized": True,
            },
        ))

        # ---------------------------------------------------------------
        # MODEL 3: Hallucination Detector — NOT TRAINED YET
        # ---------------------------------------------------------------
        cls._register(ModelInfo(
            model_id="hallucination_detector",
            name="Legal Hallucination Classifier",
            model_type=ModelType.HALLUCINATION_DETECTOR,
            purpose=(
                "Classifies AI-generated legal claims as SUPPORTED, PARTIALLY_SUPPORTED, "
                "UNSUPPORTED, CONTRADICTED, or UNVERIFIED based on retrieved evidence."
            ),
            endpoint=settings.AI_VERIFICATION_URL,
            status=ModelStatus.NOT_DEPLOYED,  # Model NOT trained — do NOT change this
            is_enabled=False,
            notes=(
                "Model has not been trained yet. Infrastructure is in place. "
                "Training data and fine-tuning approach are documented in "
                "ai-services/hallucination-detector/training/README.md"
            ),
            capabilities={
                "output_labels": [
                    "SUPPORTED", "PARTIALLY_SUPPORTED",
                    "UNSUPPORTED", "CONTRADICTED", "UNVERIFIED"
                ],
                "claim_types": [
                    "FACT", "DATE", "PERSON", "CASE_NAME", "COURT",
                    "SECTION", "ARTICLE", "CITATION", "LEGAL_PROPOSITION"
                ],
            },
        ))

        # ---------------------------------------------------------------
        # FUTURE MODELS — NOT_DEPLOYED (stubs for future expansion)
        # ---------------------------------------------------------------
        for future_model in cls._future_model_stubs():
            cls._register(future_model)

        logger.info(
            "ai_registry.initialized",
            total=len(cls._models),
            available=[mid for mid, m in cls._models.items() if m.status == ModelStatus.AVAILABLE],
            not_deployed=[mid for mid, m in cls._models.items() if m.status == ModelStatus.NOT_DEPLOYED],
        )

    @classmethod
    def _future_model_stubs(cls) -> List[ModelInfo]:
        """
        Register future models as NOT_DEPLOYED.
        This allows the system to reference them without implementing fake logic.
        """
        future_models = [
            ("ner_model", "Legal NER Model", ModelType.NER,
             "Extracts legal entities: persons, courts, judges, case numbers, acts, sections."),
            ("document_classifier", "Document Classification Model", ModelType.CLASSIFIER,
             "Classifies legal documents into petition/affidavit/notice/judgment/etc."),
            ("citation_verifier", "Citation Verification Model", ModelType.CLASSIFIER,
             "Verifies legal citations against known case law databases."),
            ("legal_similarity", "Legal Similarity Model", ModelType.SIMILARITY if hasattr(ModelType, 'SIMILARITY') else ModelType.OTHER,
             "Computes similarity between legal documents and precedents."),
            ("risk_assessor", "Legal Risk Assessment Model", ModelType.RISK_ASSESSMENT if hasattr(ModelType, 'RISK_ASSESSMENT') else ModelType.OTHER,
             "Assesses legal risk and case strength from case facts and evidence."),
            ("draft_quality", "Draft Quality Model", ModelType.CLASSIFIER,
             "Scores the quality and completeness of AI-generated legal drafts."),
            ("translation_model", "Legal Translation Model", ModelType.TRANSLATION if hasattr(ModelType, 'TRANSLATION') else ModelType.OTHER,
             "Translates legal documents between English, Hindi, and other Indian languages."),
            ("case_summarizer", "Case Summarization Model", ModelType.SUMMARIZER,
             "Generates concise case summaries from full case documents."),
            ("evidence_extractor", "Evidence Extraction Model", ModelType.NER,
             "Extracts key evidence facts from legal documents."),
            ("contradiction_detector", "Contradiction Detection Model", ModelType.CLASSIFIER,
             "Identifies logical contradictions between claims in legal documents."),
        ]
        result = []
        for mid, name, mtype, purpose in future_models:
            result.append(ModelInfo(
                model_id=mid,
                name=name,
                model_type=mtype,
                purpose=purpose,
                endpoint=None,
                status=ModelStatus.NOT_DEPLOYED,
                is_enabled=False,
                notes="This model has not been trained yet. Interface registered for future use.",
            ))
        return result

    @classmethod
    def _register(cls, model: ModelInfo) -> None:
        cls._models[model.model_id] = model

    @classmethod
    def get(cls, model_id: str) -> Optional[ModelInfo]:
        """Retrieve a model by ID."""
        return cls._models.get(model_id)

    @classmethod
    def get_all(cls) -> List[ModelInfo]:
        """Return all registered models."""
        return list(cls._models.values())

    @classmethod
    def get_available(cls) -> List[ModelInfo]:
        """Return only models that are currently AVAILABLE."""
        return [m for m in cls._models.values() if m.status == ModelStatus.AVAILABLE]

    @classmethod
    def update_status(
        cls,
        model_id: str,
        status: ModelStatus,
        latency_ms: Optional[float] = None,
    ) -> None:
        """Update a model's live status (called by health monitor)."""
        if model_id in cls._models:
            cls._models[model_id].status = status
            cls._models[model_id].last_health_check = datetime.now(timezone.utc)
            if latency_ms is not None:
                cls._models[model_id].last_latency_ms = latency_ms

    @classmethod
    def is_available(cls, model_id: str) -> bool:
        """Quick check — is the model currently available?"""
        model = cls.get(model_id)
        return model is not None and model.status == ModelStatus.AVAILABLE and model.is_enabled
