from app.mock_server import app

REQUIRED_OPERATIONS = {
    ("post", "/v1/projects"),
    ("post", "/v1/projects/{project_id}/api-keys"),
    ("delete", "/v1/projects/{project_id}/api-keys/{key_id}"),
    ("post", "/v1/ingest/batch"),
    ("post", "/v1/traces/{trace_id}/complete"),
    ("get", "/v1/traces"),
    ("get", "/v1/traces/{trace_id}"),
    ("post", "/v1/traces/{trace_id}/flags"),
    ("post", "/v1/traces/{trace_id}/analyses"),
    ("get", "/v1/jobs/{job_id}"),
    ("get", "/v1/diagnoses"),
    ("get", "/v1/diagnoses/{diagnosis_id}"),
    ("post", "/v1/diagnoses/{diagnosis_id}/feedback"),
    ("post", "/v1/eval-cases"),
    ("get", "/v1/datasets"),
    ("post", "/v1/datasets"),
    ("get", "/health"),
    ("get", "/ready"),
}


def test_contract_is_versioned_and_contains_every_mvp_operation() -> None:
    schema = app.openapi()
    operations = {
        (method, path)
        for path, path_item in schema["paths"].items()
        for method in path_item
        if method in {"get", "post", "delete", "put", "patch"}
    }

    assert schema["info"]["version"] == "1.0.0"
    assert REQUIRED_OPERATIONS <= operations
    assert schema["components"]["securitySchemes"]["ApiKeyAuth"] == {
        "type": "http",
        "description": "Project API key sent as a bearer token",
        "scheme": "bearer",
    }


def test_ingestion_contract_uses_sdk_trace_fields() -> None:
    schema = app.openapi()
    ingest_trace = schema["components"]["schemas"]["IngestTrace"]

    assert set(ingest_trace["required"]) >= {
        "trace_id",
        "project",
        "name",
        "started_at",
        "ended_at",
        "latency_ms",
    }
