import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import TypeAdapter, ValidationError

from benchmarks.schemas import FailureCategory, InjectedFault, WorkloadType


FIXTURE_PATH = Path(__file__).parent.parent / "datasets" / "injected_faults.json"
FAULTS = TypeAdapter(list[InjectedFault])


def test_injected_fault_fixtures_are_valid() -> None:
    fixtures = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    faults = FAULTS.validate_python(fixtures)

    assert len(faults) == 3
    assert {fault.workload for fault in faults} == set(WorkloadType)


def test_injected_fault_json_round_trip() -> None:
    fault = FAULTS.validate_json(FIXTURE_PATH.read_bytes())[0]

    restored = InjectedFault.model_validate_json(fault.model_dump_json())

    assert restored == fault


def test_target_span_is_backwards_compatible() -> None:
    fault = InjectedFault(
        fault_id="legacy_target_span",
        workload=WorkloadType.DOCUMENT,
        fault_type="legacy_fault",
        target_span="doc_extraction",
        expected_root_cause="doc_extraction",
        expected_failure_category=FailureCategory.SCHEMA_FAILURE,
        random_seed=404,
        created_at=datetime(2026, 1, 15, tzinfo=timezone.utc),
    )

    assert fault.target_component == "doc_extraction"


@pytest.mark.parametrize("field", ["target_component", "expected_root_cause"])
def test_invalid_component_key_is_rejected(field: str) -> None:
    values = {
        "fault_id": "invalid_component",
        "workload": "document",
        "fault_type": "invalid_component",
        "target_component": "doc_extraction",
        "expected_root_cause": "doc_extraction",
        "expected_failure_category": "schema_failure",
        "random_seed": 505,
        "created_at": "2026-01-15T12:00:00Z",
    }
    values[field] = "reranker"

    with pytest.raises(ValidationError):
        InjectedFault.model_validate(values)


def test_invalid_failure_category_is_rejected() -> None:
    with pytest.raises(ValidationError):
        InjectedFault.model_validate(
            {
                "fault_id": "invalid_category",
                "workload": "document",
                "fault_type": "invalid_category",
                "target_component": "doc_extraction",
                "expected_root_cause": "doc_extraction",
                "expected_failure_category": "not_a_category",
                "random_seed": 606,
                "created_at": "2026-01-15T12:00:00Z",
            }
        )
