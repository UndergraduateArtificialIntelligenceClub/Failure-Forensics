"""Runnable contract mock for frontend and integration development."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI, Query, Response, Security, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.api_models import (
    AnalysisCreate,
    AnalysisCreated,
    ApiKeyCreate,
    ApiKeyCreated,
    CompleteTraceResponse,
    Dataset,
    DatasetCreate,
    DatasetList,
    DiagnosisDetail,
    DiagnosisList,
    DiagnosisSummary,
    EvalCase,
    EvalCaseCreate,
    Feedback,
    FeedbackCreate,
    Flag,
    FlagCreate,
    IngestBatchRequest,
    IngestBatchResponse,
    Job,
    Project,
    ProjectCreate,
    TraceDetail,
    TraceHealth,
    TraceList,
    TraceStatus,
    TraceSummary,
)

DESCRIPTION = """Public Failure Forensics API v1 contract.

This runnable mock returns deterministic examples for frontend and integration
development. It does not persist data. Production implementations must preserve
these request and response shapes.
"""

api_key_scheme = HTTPBearer(
    auto_error=False,
    scheme_name="ApiKeyAuth",
    description="Project API key sent as a bearer token",
)


def accept_mock_api_key(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Security(api_key_scheme),
    ] = None,
) -> None:
    """Describe authentication without rejecting local mock requests."""
    del credentials


app = FastAPI(
    title="Failure Forensics API",
    version="1.0.0",
    description=DESCRIPTION,
    dependencies=[Depends(accept_mock_api_key)],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NOW = datetime(2026, 11, 27, 12, 0, tzinfo=UTC)
TRACE_ID = "0123456789abcdef0123456789abcdef"
SPAN_ID = "0123456789abcdef"


def example_trace() -> TraceSummary:
    return TraceSummary(
        id=TRACE_ID,
        project_id="proj_demo",
        external_trace_id=TRACE_ID,
        started_at=NOW,
        ended_at=NOW,
        status=TraceStatus.OK,
        health=TraceHealth.HEALTHY,
        root_span_id=SPAN_ID,
        total_latency_ms=12.5,
        total_input_tokens=20,
        total_output_tokens=8,
        estimated_cost_usd="0.000120",
        pipeline_version="v1",
    )


@app.get("/health", tags=["service"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready", tags=["service"])
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.post(
    "/v1/projects",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
    tags=["projects"],
)
def create_project(request: ProjectCreate) -> Project:
    return Project(id="proj_demo", **request.model_dump())


@app.post(
    "/v1/projects/{project_id}/api-keys",
    response_model=ApiKeyCreated,
    status_code=status.HTTP_201_CREATED,
    tags=["projects"],
)
def create_api_key(project_id: str, request: ApiKeyCreate) -> ApiKeyCreated:
    del project_id, request
    return ApiKeyCreated(id="key_demo", prefix="ff_demo", key="ff_demo_mock_secret")


@app.delete(
    "/v1/projects/{project_id}/api-keys/{key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["projects"],
)
def revoke_api_key(project_id: str, key_id: str) -> Response:
    del project_id, key_id
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post(
    "/v1/ingest/batch",
    response_model=IngestBatchResponse,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["ingestion"],
)
def ingest_batch(request: IngestBatchRequest) -> IngestBatchResponse:
    return IngestBatchResponse(
        accepted=len(request.traces),
        trace_ids=[trace.trace_id for trace in request.traces],
    )


@app.post(
    "/v1/traces/{trace_id}/complete",
    response_model=CompleteTraceResponse,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["traces"],
)
def complete_trace(trace_id: str) -> CompleteTraceResponse:
    return CompleteTraceResponse(trace_id=trace_id)


@app.get("/v1/traces", response_model=TraceList, tags=["traces"])
def list_traces(
    status_filter: Annotated[TraceStatus | None, Query(alias="status")] = None,
    health: TraceHealth | None = None,
    pipeline_version: str | None = None,
    started_after: datetime | None = None,
    started_before: datetime | None = None,
    flagged: bool | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
) -> TraceList:
    del (
        status_filter,
        health,
        pipeline_version,
        started_after,
        started_before,
        flagged,
    )
    return TraceList(items=[example_trace()], page=page, page_size=page_size, total=1)


@app.get("/v1/traces/{trace_id}", response_model=TraceDetail, tags=["traces"])
def get_trace(trace_id: str) -> TraceDetail:
    return TraceDetail(
        **example_trace().model_dump(exclude={"id", "external_trace_id"}),
        id=trace_id,
        external_trace_id=trace_id,
    )


@app.post(
    "/v1/traces/{trace_id}/flags",
    response_model=Flag,
    status_code=status.HTTP_201_CREATED,
    tags=["traces"],
)
def flag_trace(trace_id: str, request: FlagCreate) -> Flag:
    return Flag(id="flag_demo", trace_id=trace_id, **request.model_dump())


@app.post(
    "/v1/traces/{trace_id}/analyses",
    response_model=AnalysisCreated,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["analysis"],
)
def start_analysis(trace_id: str, request: AnalysisCreate) -> AnalysisCreated:
    del trace_id, request
    return AnalysisCreated(job_id="job_demo")


@app.get("/v1/jobs/{job_id}", response_model=Job, tags=["analysis"])
def get_job(job_id: str) -> Job:
    return Job(
        id=job_id,
        kind="root_cause",
        target_id=TRACE_ID,
        state="succeeded",
        progress=1,
        stage="complete",
    )


def example_diagnosis(diagnosis_id: str = "diag_demo") -> DiagnosisSummary:
    return DiagnosisSummary(
        id=diagnosis_id,
        trace_id=TRACE_ID,
        root_cause_component_key="rag.retriever",
        failure_family="retrieval",
        failure_category="missing_relevant_context",
        confidence=0.91,
        human_status="unreviewed",
    )


@app.get("/v1/diagnoses", response_model=DiagnosisList, tags=["diagnoses"])
def list_diagnoses(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
) -> DiagnosisList:
    return DiagnosisList(
        items=[example_diagnosis()], page=page, page_size=page_size, total=1
    )


@app.get(
    "/v1/diagnoses/{diagnosis_id}",
    response_model=DiagnosisDetail,
    tags=["diagnoses"],
)
def get_diagnosis(diagnosis_id: str) -> DiagnosisDetail:
    return DiagnosisDetail(
        **example_diagnosis(diagnosis_id).model_dump(),
        root_cause_span_id=SPAN_ID,
        explanation="The retriever omitted the relevant source document.",
        propagation_path=[SPAN_ID],
        grounded=True,
    )


@app.post(
    "/v1/diagnoses/{diagnosis_id}/feedback",
    response_model=Feedback,
    status_code=status.HTTP_201_CREATED,
    tags=["diagnoses"],
)
def create_feedback(diagnosis_id: str, request: FeedbackCreate) -> Feedback:
    return Feedback(
        id="feedback_demo", diagnosis_id=diagnosis_id, decision=request.decision
    )


@app.post(
    "/v1/eval-cases",
    response_model=EvalCase,
    status_code=status.HTTP_201_CREATED,
    tags=["evaluation"],
)
def create_eval_case(request: EvalCaseCreate) -> EvalCase:
    return EvalCase(
        id="case_demo",
        dataset_id=request.dataset_id,
        source_trace_id=request.source_trace_id,
        expected_behavior=request.expected_behavior,
        created_from=request.created_from,
    )


@app.get("/v1/datasets", response_model=DatasetList, tags=["evaluation"])
def list_datasets(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
) -> DatasetList:
    dataset = Dataset(
        id="dataset_demo",
        project_id="proj_demo",
        name="Demo failures",
        kind="failure",
        version=1,
    )
    return DatasetList(items=[dataset], page=page, page_size=page_size, total=1)


@app.post(
    "/v1/datasets",
    response_model=Dataset,
    status_code=status.HTTP_201_CREATED,
    tags=["evaluation"],
)
def create_dataset(request: DatasetCreate) -> Dataset:
    return Dataset(id="dataset_demo", version=1, **request.model_dump())
