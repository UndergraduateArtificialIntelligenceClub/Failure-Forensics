# OpenAPI v1 contract and mock server

**Jira:** [KAN-35](https://pranav01.atlassian.net/browse/KAN-35)

The versioned API contract is committed at `openapi/openapi-v1.json`. It covers
all MVP operations in the data-model API table, including projects and API keys,
ingestion, traces, analysis jobs, diagnoses, feedback, evaluation cases, datasets,
and service health.

Authenticated clients send the project API key as a bearer token in the
`Authorization` header. The local mock documents this security scheme but accepts
requests without a credential so frontend development does not need a real key.

The mock is intentionally non-persistent. It gives the frontend deterministic
responses while the production endpoints are implemented in their own Jira
stories.

## Run the mock

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e "./backend[dev]"
PYTHONPATH=backend uvicorn app.mock_server:app --reload
```

The service is available at `http://localhost:8000`, interactive documentation
at `http://localhost:8000/docs`, and the live schema at
`http://localhost:8000/openapi.json`.

The frontend uses `NEXT_PUBLIC_API_URL=http://localhost:8000`, as shown in
`frontend/.env.example`. The mock allows browser requests from the local Next.js
development origins on port 3000.

## Update the contract

The FastAPI models are the executable source for the published JSON file.

```bash
PYTHONPATH=backend python scripts/export_openapi.py
PYTHONPATH=backend python scripts/export_openapi.py --check
```

Contract tests fail when an MVP operation is missing, and CI fails when the
committed JSON is stale.
