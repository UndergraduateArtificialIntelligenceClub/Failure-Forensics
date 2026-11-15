"""Frozen M0 trace, span, and data-flow link contract."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

TRACE_ID_PATTERN = r"^[0-9a-f]{32}$"
SPAN_ID_PATTERN = r"^[0-9a-f]{16}$"


class TraceStatus(StrEnum):
    OK = "ok"
    ERROR = "error"
    INCOMPLETE = "incomplete"


class SpanStatus(StrEnum):
    OK = "ok"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class SpanType(StrEnum):
    LLM = "llm"
    RETRIEVAL = "retrieval"
    RERANKER = "reranker"
    TOOL = "tool"
    AGENT = "agent"
    TRANSFORM = "transform"
    GUARDRAIL = "guardrail"
    CUSTOM = "custom"


class SpanLinkRelation(StrEnum):
    CONSUMES_OUTPUT_OF = "consumes_output_of"
    RETRIES = "retries"
    FOLLOWS = "follows"


class ErrorDetails(BaseModel):
    """Operational error captured from a trace or span."""

    model_config = ConfigDict(extra="forbid")

    type: str = Field(min_length=1)
    message: str


class SpanLink(BaseModel):
    """Directed relationship from a producer span to a consumer span."""

    model_config = ConfigDict(extra="forbid")

    from_span_id: str = Field(pattern=SPAN_ID_PATTERN)
    to_span_id: str = Field(pattern=SPAN_ID_PATTERN)
    relation: SpanLinkRelation = SpanLinkRelation.CONSUMES_OUTPUT_OF

    @model_validator(mode="after")
    def reject_self_link(self) -> SpanLink:
        if self.from_span_id == self.to_span_id:
            raise ValueError("a span link cannot point to the same span")
        return self


class Span(BaseModel):
    """One operation in a trace."""

    model_config = ConfigDict(extra="forbid")

    trace_id: str = Field(pattern=TRACE_ID_PATTERN)
    span_id: str = Field(pattern=SPAN_ID_PATTERN)
    parent_span_id: str | None = Field(default=None, pattern=SPAN_ID_PATTERN)
    name: str = Field(min_length=1)
    type: SpanType = SpanType.CUSTOM
    component_key: str | None = None
    started_at: datetime
    ended_at: datetime
    latency_ms: float = Field(ge=0)
    status: SpanStatus = SpanStatus.OK
    input: Any = None
    output: Any = None
    input_ref: str | None = None
    output_ref: str | None = None
    prompt_ref: str | None = None
    raw_response_ref: str | None = None
    model_provider: str | None = None
    model_name: str | None = None
    prompt_version: str | None = None
    component_version: str | None = None
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    estimated_cost_usd: float | None = Field(default=None, ge=0)
    error: ErrorDetails | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_timing_and_parent(self) -> Span:
        if self.ended_at < self.started_at:
            raise ValueError("ended_at must be at or after started_at")
        if self.parent_span_id == self.span_id:
            raise ValueError("a span cannot be its own parent")
        return self


class Trace(BaseModel):
    """One complete end-to-end execution and its data-flow graph."""

    model_config = ConfigDict(extra="forbid")

    trace_id: str = Field(pattern=TRACE_ID_PATTERN)
    project: str = Field(min_length=1)
    name: str = Field(min_length=1)
    pipeline_version: str | None = None
    started_at: datetime
    ended_at: datetime
    latency_ms: float = Field(ge=0)
    status: TraceStatus = TraceStatus.OK
    error: ErrorDetails | None = None
    spans: list[Span] = Field(default_factory=list)
    links: list[SpanLink] = Field(default_factory=list)
    tags: dict[str, str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_trace_graph(self) -> Trace:
        if self.ended_at < self.started_at:
            raise ValueError("ended_at must be at or after started_at")

        span_ids = [span.span_id for span in self.spans]
        if len(span_ids) != len(set(span_ids)):
            raise ValueError("span_id values must be unique within a trace")

        known_span_ids = set(span_ids)
        for span in self.spans:
            if span.trace_id != self.trace_id:
                raise ValueError("every span must use the containing trace_id")
            if (
                span.parent_span_id is not None
                and span.parent_span_id not in known_span_ids
            ):
                raise ValueError("parent_span_id must reference a span in the trace")

        for link in self.links:
            if link.from_span_id not in known_span_ids:
                raise ValueError("from_span_id must reference a span in the trace")
            if link.to_span_id not in known_span_ids:
                raise ValueError("to_span_id must reference a span in the trace")

        return self


__all__ = [
    "ErrorDetails",
    "Span",
    "SpanLink",
    "SpanLinkRelation",
    "SpanStatus",
    "SpanType",
    "Trace",
    "TraceStatus",
]
