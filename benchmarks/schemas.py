"""Pydantic schemas for benchmark data."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator

from benchmarks.constants import WorkloadAKeys, WorkloadBKeys, WorkloadCKeys


class WorkloadType(str, Enum):
    DOCUMENT = "document"
    RAG = "rag"
    AGENT = "agent"


class FailureCategory(str, Enum):
    HALLUCINATION = "hallucination"
    INSTRUCTION_FAILURE = "instruction_failure"
    FORMAT_FAILURE = "format_failure"
    REASONING_FAILURE = "reasoning_failure"
    REFUSAL_ERROR = "refusal_error"
    CONFIDENCE_MISMATCH = "confidence_mismatch"

    RETRIEVAL_MISS = "retrieval_miss"
    IRRELEVANT_RETRIEVAL = "irrelevant_retrieval"
    RERANKING_FAILURE = "reranking_failure"
    CONTEXT_POLLUTION = "context_pollution"
    CONTEXT_OVERFLOW = "context_overflow"
    CITATION_FAILURE = "citation_failure"

    PLANNING_FAILURE = "planning_failure"
    TOOL_SELECTION_FAILURE = "tool_selection_failure"
    TOOL_ARGUMENT_FAILURE = "tool_argument_failure"
    TOOL_EXECUTION_FAILURE = "tool_execution_failure"
    LOOP_FAILURE = "loop_failure"
    PREMATURE_TERMINATION = "premature_termination"

    CONTEXT_LOSS = "context_loss"
    SCHEMA_FAILURE = "schema_failure"
    DEPENDENCY_FAILURE = "dependency_failure"
    TIMEOUT = "timeout"

    PROMPT_REGRESSION = "prompt_regression"
    MODEL_REGRESSION = "model_regression"
    PARAMETER_REGRESSION = "parameter_regression"
    TOKEN_LIMIT_FAILURE = "token_limit_failure"

    INGESTION_FAILURE = "ingestion_failure"
    STORAGE_FAILURE = "storage_failure"
    EVALUATOR_FAILURE = "evaluator_failure"
    QUEUE_FAILURE = "queue_failure"
    PROVIDER_OUTAGE = "provider_outage"


WORKLOAD_COMPONENT_KEYS: dict[WorkloadType, frozenset[str]] = {
    WorkloadType.DOCUMENT: frozenset(key.value for key in WorkloadAKeys),
    WorkloadType.RAG: frozenset(key.value for key in WorkloadBKeys),
    WorkloadType.AGENT: frozenset(key.value for key in WorkloadCKeys),
}


class InjectedFault(BaseModel):
    """A benchmark fault injection and its expected diagnosis."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    fault_id: str = Field(min_length=1)
    workload: WorkloadType
    fault_type: str = Field(min_length=1)
    target_component: str = Field(
        min_length=1,
        validation_alias=AliasChoices("target_component", "target_span"),
    )
    injection_parameters: dict[str, Any] = Field(default_factory=dict)
    expected_root_cause: str = Field(min_length=1)
    expected_failure_category: FailureCategory
    expected_downstream_impact: list[str] = Field(default_factory=list)
    random_seed: int
    created_at: datetime

    @model_validator(mode="after")
    def validate_component_keys(self) -> "InjectedFault":
        valid_keys = WORKLOAD_COMPONENT_KEYS[self.workload]
        component_fields = {
            "target_component": self.target_component,
            "expected_root_cause": self.expected_root_cause,
        }
        invalid_components = [
            f"{field}={value!r}"
            for field, value in component_fields.items()
            if value not in valid_keys
        ]
        invalid_components.extend(
            f"expected_downstream_impact={value!r}"
            for value in self.expected_downstream_impact
            if value not in valid_keys
        )
        if invalid_components:
            raise ValueError(
                f"Invalid component key(s) for workload {self.workload.value}: "
                + ", ".join(invalid_components)
            )
        return self
