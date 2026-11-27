from app.mock_server import app
from failure_forensics import Forensics
from fastapi.testclient import TestClient


def test_sdk_trace_reaches_ingestion_contract() -> None:
    responses: list[tuple[int, dict[str, object]]] = []

    with TestClient(app) as client:

        def export(trace: dict[str, object]) -> None:
            response = client.post("/v1/ingest/batch", json={"traces": [trace]})
            responses.append((response.status_code, response.json()))

        ff = Forensics(project="integration-review", exporter=export)

        @ff.trace("sdk-to-ingestion", pipeline_version="sprint-2")
        def pipeline() -> None:
            with ff.span("retrieve", type="retrieval") as span:
                span.set_output({"documents": ["demo"]})

        pipeline()

    assert len(responses) == 1
    status_code, body = responses[0]
    assert status_code == 202
    assert body["accepted"] == 1
    assert body["trace_ids"]
