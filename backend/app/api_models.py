"""Version 1 API request and response models.

These models are shared by the contract mock and the generated OpenAPI document.
They intentionally describe the public boundary without implementing persistence.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TraceStatus(StrEnum):
    OK = "ok"
    ERROR = "error"
    INCOMPLETE = "incomplete"


class TraceHealth(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"


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


class ErrorDetails(ApiModel):
    type: str
    message: str


class SpanLink(ApiModel):
    from_span_id: str
    to_span_id: str
    relation: Literal["consumes_output_of", "retries", "follows"] = "consumes_output_of"


class IngestSpan(ApiModel):
    trace_id: str
    span_id: str
    parent_span_id: str | None = None
    name: str
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


class IngestTrace(ApiModel):
    trace_id: str
    project: str
    name: str
    pipeline_version: str | None = None
    started_at: datetime
    ended_at: datetime
    latency_ms: float = Field(ge=0)
    status: TraceStatus = TraceStatus.OK
    error: ErrorDetails | None = None
    spans: list[IngestSpan] = Field(default_factory=list)
    links: list[SpanLink] = Field(default_factory=list)
    tags: dict[str, str] = Field(default_factory=dict)


class TraceSpan(ApiModel):
    id: str
    trace_id: str
    parent_span_id: str | None = None
    name: str
    component_key: str
    type: SpanType
    started_at: datetime
    ended_at: datetime | None = None
    latency_ms: float | None = Field(default=None, ge=0)
    status: SpanStatus
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
    estimated_cost_usd: str | None = None
    error_type: str | None = None
    error_message: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)


class IngestBatchRequest(ApiModel):
    traces: list[IngestTrace] = Field(min_length=1, max_length=100)


class IngestBatchResponse(ApiModel):
    accepted: int
    trace_ids: list[str]


class ProjectCreate(ApiModel):
    name: str = Field(min_length=1)
    capture_policy: Literal["metadata", "sampled_payloads", "full_payloads"] = (
        "metadata"
    )
    retention_days: int = Field(default=30, ge=1, le=365)


class Project(ApiModel):
    id: str
    name: str
    capture_policy: str
    retention_days: int


class ApiKeyCreate(ApiModel):
    name: str = Field(default="default", min_length=1)


class ApiKeyCreated(ApiModel):
    id: str
    prefix: str
    key: str = Field(description="Secret returned once and never stored in plaintext")


class TraceSummary(ApiModel):
    id: str
    project_id: str
    external_trace_id: str | None = None
    started_at: datetime
    ended_at: datetime | None = None
    status: TraceStatus
    health: TraceHealth
    root_span_id: str | None = None
    total_latency_ms: float | None = None
    total_input_tokens: int | None = None
    total_output_tokens: int | None = None
    estimated_cost_usd: str | None = None
    pipeline_version: str
    git_commit: str | None = None
    tags: dict[str, Any] = Field(default_factory=dict)
    feedback_status: Literal["none", "flagged", "reviewed"] = "none"


class TraceList(ApiModel):
    items: list[TraceSummary]
    page: int
    page_size: int
    total: int


class TraceDetail(TraceSummary):
    spans: list[TraceSpan] = Field(default_factory=list)
    links: list[SpanLink] = Field(default_factory=list)


class CompleteTraceResponse(ApiModel):
    trace_id: str
    state: Literal["queued"] = "queued"


class FlagCreate(ApiModel):
    span_id: str | None = None
    reason: str = Field(min_length=1)
    source: Literal["user", "api", "detector"] = "user"


class Flag(ApiModel):
    id: str
    trace_id: str
    span_id: str | None = None
    reason: str
    source: str


class AnalysisCreate(ApiModel):
    kind: Literal["root_cause"] = "root_cause"


class Job(ApiModel):
    id: str
    kind: str
    target_id: str
    state: Literal["queued", "running", "succeeded", "failed", "cancelled"]
    progress: float = Field(ge=0, le=1)
    stage: str
    error: str | None = None


class AnalysisCreated(ApiModel):
    job_id: str
    state: Literal["queued"] = "queued"


class DiagnosisSummary(ApiModel):
    id: str
    trace_id: str
    root_cause_component_key: str
    failure_family: str
    failure_category: str
    confidence: float = Field(ge=0, le=1)
    human_status: Literal["unreviewed", "confirmed", "corrected", "unsure"]


class DiagnosisList(ApiModel):
    items: list[DiagnosisSummary]
    page: int
    page_size: int
    total: int


class DiagnosisDetail(DiagnosisSummary):
    root_cause_span_id: str
    explanation: str
    propagation_path: list[str]
    grounded: bool


class FeedbackCreate(ApiModel):
    decision: Literal["confirm", "correct", "unsure"]
    corrected_span_id: str | None = None
    corrected_category: str | None = None
    note: str | None = None


class Feedback(ApiModel):
    id: str
    diagnosis_id: str
    decision: str


class EvalCaseCreate(ApiModel):
    dataset_id: str
    source_trace_id: str | None = None
    expected_behavior: str
    expected_root_cause_component: str | None = None
    expected_failure_category: str | None = None
    created_from: Literal[
        "human_confirmed", "injected_fault", "curated", "fixed_regression"
    ]


class EvalCase(ApiModel):
    id: str
    dataset_id: str
    source_trace_id: str | None = None
    expected_behavior: str
    created_from: str


class DatasetCreate(ApiModel):
    project_id: str
    name: str = Field(min_length=1)
    kind: Literal["golden", "failure", "injected"]


class Dataset(ApiModel):
    id: str
    project_id: str
    name: str
    kind: str
    version: int


class DatasetList(ApiModel):
    items: list[Dataset]
    page: int
    page_size: int
    total: int
