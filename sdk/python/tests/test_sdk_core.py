"""Unit tests for the Failure Forensics SDK core engine.

Verifies span context management, parent-child nesting, input linking,
error propagation, and decorator trace context propagation.
"""

import pytest

from failure_forensics.client import Forensics
from failure_forensics.context import get_current_parent_id
from failure_forensics.models import SpanStatus
from failure_forensics.span import SpanContextManager


def test_nested_spans_get_correct_parent():
    assert get_current_parent_id() is None
    with SpanContextManager("outer") as outer:
        assert get_current_parent_id() == outer.span_id
        with SpanContextManager("inner") as inner:
            assert inner.parent_span_id == outer.span_id
        assert get_current_parent_id() == outer.span_id
    assert get_current_parent_id() is None


def test_inputs_from_creates_span_link():
    with SpanContextManager("producer") as producer:
        producer.set_output({"value": 1})

    consumer = SpanContextManager("consumer", inputs_from=[producer])
    with consumer:
        pass

    assert len(consumer.links) == 1
    assert consumer.links[0].from_span_id == producer.span_id
    assert consumer.links[0].to_span_id == consumer.span_id


def test_exception_recorded_as_error():
    client = Forensics(project="demo", api_key="test-key")

    with pytest.raises(ValueError, match="boom"):
        with client.span("failing_step"):
            raise ValueError("boom")

    assert len(client.buffer) == 1
    recorded = client.buffer[0]
    assert recorded.status == SpanStatus.ERROR
    assert recorded.error is not None
    assert recorded.error.type == "ValueError"
    assert recorded.error.message == "boom"


def test_nested_trace_decorator_shares_trace_id():
    client = Forensics(project="demo", api_key="test-key")

    @client.trace(name="child_fn")
    def child_fn(x: int) -> int:
        return x + 1

    @client.trace(name="parent_fn")
    def parent_fn(x: int) -> int:
        return child_fn(x) * 2

    assert parent_fn(3) == 8
    assert len(client.buffer) == 2
    assert client.buffer[0].trace_id == client.buffer[1].trace_id
    assert client.buffer[0].parent_span_id == client.buffer[1].span_id
