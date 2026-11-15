from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from failure_forensics import Span, SpanLink, Trace
from failure_forensics.models import SpanLinkRelation

TRACE_ID = "a" * 32
PRODUCER_ID = "1" * 16
CONSUMER_ID = "2" * 16
STARTED_AT = datetime(2026, 11, 13, tzinfo=UTC)
ENDED_AT = STARTED_AT + timedelta(milliseconds=12)


def make_span(default_span_id: str, **overrides: object) -> Span:
    values: dict[str, object] = {
        "trace_id": TRACE_ID,
        "span_id": default_span_id,
        "name": "operation",
        "component_key": "rag.operation",
        "started_at": STARTED_AT,
        "ended_at": ENDED_AT,
        "latency_ms": 12,
    }
    values.update(overrides)
    return Span.model_validate(values)


def test_trace_span_and_link_contract_accepts_data_flow_graph() -> None:
    producer = make_span(PRODUCER_ID, type="retrieval")
    consumer = make_span(
        CONSUMER_ID,
        type="llm",
        parent_span_id=PRODUCER_ID,
        input_tokens=20,
        output_tokens=5,
    )
    link = SpanLink(
        from_span_id=PRODUCER_ID,
        to_span_id=CONSUMER_ID,
        relation=SpanLinkRelation.CONSUMES_OUTPUT_OF,
    )

    trace = Trace(
        trace_id=TRACE_ID,
        project="failure-forensics",
        name="rag-pipeline",
        pipeline_version="v1",
        started_at=STARTED_AT,
        ended_at=ENDED_AT,
        latency_ms=12,
        spans=[producer, consumer],
        links=[link],
    )

    assert trace.links[0].from_span_id == producer.span_id
    assert trace.links[0].to_span_id == consumer.span_id
    assert trace.spans[1].parent_span_id == producer.span_id


@pytest.mark.parametrize(
    ("field", "value"),
    [("trace_id", "not-hex"), ("span_id", "short")],
)
def test_span_rejects_invalid_identifiers(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        make_span(PRODUCER_ID, **{field: value})


def test_trace_rejects_links_to_unknown_spans() -> None:
    producer = make_span(PRODUCER_ID)
    link = SpanLink(from_span_id=PRODUCER_ID, to_span_id=CONSUMER_ID)

    with pytest.raises(ValidationError, match="to_span_id"):
        Trace(
            trace_id=TRACE_ID,
            project="failure-forensics",
            name="invalid-graph",
            started_at=STARTED_AT,
            ended_at=ENDED_AT,
            latency_ms=12,
            spans=[producer],
            links=[link],
        )


def test_span_rejects_negative_latency_and_reversed_timestamps() -> None:
    with pytest.raises(ValidationError):
        make_span(PRODUCER_ID, latency_ms=-1)

    with pytest.raises(ValidationError, match="ended_at"):
        make_span(PRODUCER_ID, ended_at=STARTED_AT - timedelta(seconds=1))


def test_contract_forbids_unreviewed_fields() -> None:
    with pytest.raises(ValidationError, match="extra_forbidden"):
        make_span(PRODUCER_ID, unreviewed_field="value")
