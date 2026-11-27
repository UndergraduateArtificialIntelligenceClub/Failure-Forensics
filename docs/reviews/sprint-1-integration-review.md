# Sprint 1 integration review

**Jira:** [KAN-36](https://pranav01.atlassian.net/browse/KAN-36)<br>
**Reviewed:** 27 November 2026

## Result

The frozen Sprint 1 SDK contract connects successfully to the Sprint 2 v1
ingestion boundary. A trace created with `Forensics`, including its spans and
links, validates in the SDK and is accepted by `POST /v1/ingest/batch`.

Run the demo from the repository root after installing both Python packages:

```bash
pip install -e "./backend[dev]" -e "./sdk/python[dev]"
PYTHONPATH=backend:sdk/python python scripts/demo_sdk_ingestion.py
```

Expected output:

```text
accepted=1 trace_id=<32-character trace id>
```

The same path is covered automatically by
`tests/integration/test_sdk_ingestion.py` in App CI.

## Interfaces reviewed

| Producer | Boundary | Consumer | Result |
|---|---|---|---|
| Python SDK | Frozen Trace, Span, and SpanLink payload | Batch ingestion request | Pass |
| API mock | OpenAPI 3.1 schema | Frontend typed client | Ready for client regeneration |
| Local frontend | `NEXT_PUBLIC_API_URL` | Contract mock with CORS | Pass |

## Issues and follow-ups

No blocking Sprint 1 integration issue remains after adding the batch envelope
and integration test. Production persistence and idempotent upsert remain in
[KAN-39](https://pranav01.atlassian.net/browse/KAN-39), and the background HTTP
exporter remains in [KAN-38](https://pranav01.atlassian.net/browse/KAN-38).
Those are planned Sprint 2 implementations, not blockers in the frozen Sprint 1
contract.
