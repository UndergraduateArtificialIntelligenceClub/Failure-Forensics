"""Demonstrate the Sprint 1 SDK exporting to the API v1 mock ingestion path."""

from __future__ import annotations

from typing import Any

from app.mock_server import app
from failure_forensics import Forensics
from fastapi.testclient import TestClient


def main() -> None:
    with TestClient(app) as client:

        def export(trace: dict[str, Any]) -> None:
            response = client.post("/v1/ingest/batch", json={"traces": [trace]})
            response.raise_for_status()
            print(
                f"accepted={response.json()['accepted']} "
                f"trace_id={response.json()['trace_ids'][0]}"
            )

        ff = Forensics(project="integration-review", exporter=export)

        @ff.trace("sdk-to-ingestion", pipeline_version="sprint-2")
        def pipeline() -> None:
            with ff.span("retrieve", type="retrieval") as span:
                span.set_output({"documents": ["demo"]})

        pipeline()


if __name__ == "__main__":
    main()
