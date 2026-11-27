import pytest
from app.mock_server import TRACE_ID, app
from fastapi.testclient import TestClient


def test_mock_server_exposes_contract_and_frontend_cors() -> None:
    with TestClient(app) as client:
        contract = client.get("/openapi.json")
        health = client.get(
            "/health",
            headers={"Origin": "http://localhost:3000"},
        )

    assert contract.status_code == 200
    assert contract.json()["info"]["version"] == "1.0.0"
    assert health.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_mock_ingestion_accepts_a_frozen_sdk_payload() -> None:
    payload = {
        "traces": [
            {
                "trace_id": TRACE_ID,
                "project": "demo",
                "name": "rag-pipeline",
                "started_at": "2026-11-27T12:00:00Z",
                "ended_at": "2026-11-27T12:00:01Z",
                "latency_ms": 1000,
                "status": "ok",
                "spans": [],
                "links": [],
                "tags": {},
            }
        ]
    }

    with TestClient(app) as client:
        response = client.post("/v1/ingest/batch", json=payload)

    assert response.status_code == 202
    assert response.json() == {"accepted": 1, "trace_ids": [TRACE_ID]}


def test_mock_server_returns_frontend_trace_list_shape() -> None:
    with TestClient(app) as client:
        response = client.get("/v1/traces?page=1&page_size=25")

    assert response.status_code == 200
    assert response.json() == {
        "items": [
            {
                "id": TRACE_ID,
                "project_id": "proj_demo",
                "external_trace_id": TRACE_ID,
                "started_at": "2026-11-27T12:00:00Z",
                "ended_at": "2026-11-27T12:00:00Z",
                "status": "ok",
                "health": "healthy",
                "root_span_id": "0123456789abcdef",
                "total_latency_ms": 12.5,
                "total_input_tokens": 20,
                "total_output_tokens": 8,
                "estimated_cost_usd": "0.000120",
                "pipeline_version": "v1",
                "git_commit": None,
                "tags": {},
                "feedback_status": "none",
            }
        ],
        "page": 1,
        "page_size": 25,
        "total": 1,
    }


@pytest.mark.parametrize(
    ("method", "path", "body", "expected_status"),
    [
        (
            "post",
            "/v1/projects",
            {"name": "Demo", "capture_policy": "metadata", "retention_days": 30},
            201,
        ),
        (
            "post",
            "/v1/projects/proj_demo/api-keys",
            {"name": "frontend"},
            201,
        ),
        ("delete", "/v1/projects/proj_demo/api-keys/key_demo", None, 204),
        ("post", f"/v1/traces/{TRACE_ID}/complete", None, 202),
        ("get", f"/v1/traces/{TRACE_ID}", None, 200),
        (
            "post",
            f"/v1/traces/{TRACE_ID}/flags",
            {"reason": "Wrong answer"},
            201,
        ),
        (
            "post",
            f"/v1/traces/{TRACE_ID}/analyses",
            {"kind": "root_cause"},
            202,
        ),
        ("get", "/v1/jobs/job_demo", None, 200),
        ("get", "/v1/diagnoses", None, 200),
        ("get", "/v1/diagnoses/diag_demo", None, 200),
        (
            "post",
            "/v1/diagnoses/diag_demo/feedback",
            {"decision": "confirm"},
            201,
        ),
        (
            "post",
            "/v1/eval-cases",
            {
                "dataset_id": "dataset_demo",
                "expected_behavior": "Return a grounded answer",
                "created_from": "curated",
            },
            201,
        ),
        ("get", "/v1/datasets", None, 200),
        (
            "post",
            "/v1/datasets",
            {"project_id": "proj_demo", "name": "Failures", "kind": "failure"},
            201,
        ),
        ("get", "/ready", None, 200),
    ],
)
def test_every_mvp_mock_operation_responds(
    method: str,
    path: str,
    body: dict[str, object] | None,
    expected_status: int,
) -> None:
    with TestClient(app) as client:
        response = client.request(method, path, json=body)

    assert response.status_code == expected_status, response.text
