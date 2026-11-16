"""Pydantic schemas for benchmark data."""

from enum import Enum
from typing import Any

from app.detection.taxonomy import FailureCategory
from pydantic import AliasChoices, BaseModel, ConfigDict, Field, model_validator

from benchmarks.constants import WorkloadAKeys, WorkloadBKeys, WorkloadCKeys


class WorkloadType(str, Enum):
    DOCUMENT = "document"
    RAG = "rag"
    AGENT = "agent"


class DatasetSplit(str, Enum):
    DEV = "dev"
    HELDOUT = "heldout"


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
    target_component_key: str = Field(
        min_length=1,
        validation_alias=AliasChoices(
            "target_component_key", "target_component", "target_span"
        ),
    )
    injection_parameters: dict[str, Any] = Field(default_factory=dict)
    expected_root_cause_component: str = Field(
        min_length=1,
        validation_alias=AliasChoices(
            "expected_root_cause_component", "expected_root_cause"
        ),
    )
    expected_failure_category: FailureCategory
    expected_downstream_impact: list[str] = Field(default_factory=list)
    random_seed: int
    split: DatasetSplit

    @model_validator(mode="after")
    def validate_component_keys(self) -> "InjectedFault":
        valid_keys = WORKLOAD_COMPONENT_KEYS[self.workload]
        component_fields = {
            "target_component_key": self.target_component_key,
            "expected_root_cause_component": self.expected_root_cause_component,
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
