import json
import re
from pathlib import Path
from typing import Any

import pytest
from app.detection.taxonomy import FailureCategory, FailureFamily

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "rca"
FIXTURE_PATHS = sorted(FIXTURE_DIR.glob("*.json"))
HEX_16 = re.compile(r"^[0-9a-f]{16}$")
HEX_32 = re.compile(r"^[0-9a-f]{32}$")
COMPONENT_KEY = re.compile(r"^(doc|rag)\.[a-z][a-z0-9_]*$")
ROLES = {
    "healthy",
    "root_cause",
    "propagated",
    "degraded",
    "failed_output",
    "unknown",
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _badness(signals: list[dict[str, Any]], status: str) -> float | None:
    """Reference for the Step 2 pass/fail precedence contract."""
    scores = [1.0] if status in {"error", "timeout"} else []
    for signal in signals:
        verdict = signal["verdict"]
        if verdict in {"fail", "review"}:
            multiplier = 1.0 if verdict == "fail" else 0.5
            scores.append(signal["confidence"] * multiplier)
    if scores:
        return max(scores)
    if any(signal["verdict"] == "pass" for signal in signals):
        return 0.0
    return None


def test_fixture_set_covers_document_and_rag_cases() -> None:
    fixtures = [_load(path) for path in FIXTURE_PATHS]

    assert len(fixtures) >= 6
    assert {fixture["workload"] for fixture in fixtures} == {"document", "rag"}
    assert len({fixture["fixture_id"] for fixture in fixtures}) == len(fixtures)


@pytest.mark.parametrize("path", FIXTURE_PATHS, ids=lambda path: path.stem)
def test_fixture_contract(path: Path) -> None:
    fixture = _load(path)
    trace = fixture["trace"]
    spans = fixture["spans"]
    links = fixture["links"]
    signals = fixture["signals"]
    flags = fixture["flags"]
    expected = fixture["expected"]

    assert fixture["fixture_format"] == 1
    assert HEX_32.fullmatch(trace["id"])

    span_ids = {span["id"] for span in spans}
    component_keys = {span["component_key"] for span in spans}
    assert len(span_ids) == len(spans)
    assert len(component_keys) == len(spans)
    assert trace["root_span_id"] in span_ids
    assert all(HEX_16.fullmatch(span_id) for span_id in span_ids)
    assert all(COMPONENT_KEY.fullmatch(key) for key in component_keys)
    assert all(span["trace_id"] == trace["id"] for span in spans)
    assert all(
        span["parent_span_id"] is None or span["parent_span_id"] in span_ids
        for span in spans
    )

    assert all(link["from_span_id"] in span_ids for link in links)
    assert all(link["to_span_id"] in span_ids for link in links)
    assert all(link["relation"] == "consumes_output_of" for link in links)
    assert all(signal["trace_id"] == trace["id"] for signal in signals)
    assert all(
        signal["span_id"] is None or signal["span_id"] in span_ids for signal in signals
    )
    assert all(flag["trace_id"] == trace["id"] for flag in flags)
    assert all(flag["span_id"] is None or flag["span_id"] in span_ids for flag in flags)

    categories = {category.value for category in FailureCategory}
    families = {family.value for family in FailureFamily}
    signal_categories = {
        signal["failure_category"]
        for signal in signals
        if signal.get("failure_category") is not None
    }
    signal_families = {
        signal["failure_family"]
        for signal in signals
        if signal.get("failure_family") is not None
    }
    assert signal_categories <= categories
    assert signal_families <= families

    assert set(expected["span_roles"]) == component_keys
    assert set(expected["span_roles"].values()) <= ROLES
    if expected["status"] == "no_failure":
        assert expected["root_cause_component"] is None
        assert expected["propagation_path"] == []
    else:
        root = expected["root_cause_component"]
        assert root in component_keys
        assert expected["failure_category"] in categories
        assert expected["failure_family"] in families
        assert expected["propagation_path"][0] == root
        assert set(expected["propagation_path"]) <= component_keys

    fault = fixture["fault"]
    if fault is not None:
        assert fault["target_component_key"] in component_keys
        assert COMPONENT_KEY.fullmatch(fault["target_component_key"])


def test_doc_01_pass_only_classification_is_healthy() -> None:
    fixture = _load(FIXTURE_DIR / "doc-01-hallucinated-entity.json")
    classification = next(
        span
        for span in fixture["spans"]
        if span["component_key"] == "doc.classification"
    )
    signals = [
        signal
        for signal in fixture["signals"]
        if signal["span_id"] == classification["id"]
    ]

    assert _badness(signals, classification["status"]) == 0.0
    assert fixture["expected"]["span_roles"]["doc.classification"] == "healthy"


def test_failure_evidence_wins_over_pass_evidence() -> None:
    signals = [
        {"verdict": "pass", "confidence": 1.0},
        {"verdict": "fail", "confidence": 0.8},
    ]
    assert _badness(signals, "ok") == 0.8
