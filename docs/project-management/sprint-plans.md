# Sprint Plans

The project runs **8 two-week sprints** from 2 Nov 2026 to 26 Feb 2027, with a holiday break from 24 Dec to 3 Jan. Code is complete on **26 Feb**. The final demo is in the **first or second week of March 2027**; the days between 26 Feb and the demo are for rehearsals and bug fixes only.

| Sprint | Dates | Theme | Points | Milestone |
|---|---|---|---|---|
| [S1](#sprint-1) | 2 Nov 2026 → 13 Nov 2026 | Definition & Architecture | 60 | **M0 Architecture freeze (13 Nov)** |
| [S2](#sprint-2) | 16 Nov 2026 → 27 Nov 2026 | SDK & Core Trace | 67 |  |
| [S3](#sprint-3) | 30 Nov 2026 → 11 Dec 2026 | Trace Platform | 59 | **M1 Vertical slice (11 Dec)** |
| [S4](#sprint-4) | 14 Dec 2026 → 23 Dec 2026 | AI Integrations & Detection base (short sprint) | 35 |  |
| [S5](#sprint-5) | 4 Jan 2027 → 15 Jan 2027 | Detection | 58 |  |
| [S6](#sprint-6) | 18 Jan 2027 → 29 Jan 2027 | Forensics | 61 | **M2 MVP (29 Jan)** |
| [S7](#sprint-7) | 1 Feb 2027 → 12 Feb 2027 | Evidence, Review & Evaluation | 74 | **M3 Feature freeze (12 Feb)** |
| [S8](#sprint-8) | 15 Feb 2027 → 26 Feb 2027 | Hardening, Report & Demo prep | 79 | **M4 Code complete / release candidate (26 Feb)** |
| Demo | Week of 1 or 8 Mar 2027 | Final demo | | **Live demo** |

## Points per person

| Owner | Role | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 | Tech Lead & Architect | 12 | 7 | 5 | 2 | 5 | 6 | 4 | 10 | 51 |
| T2 | SDK & Ingestion | 6 | 13 | 13 | 5 | 8 | 8 | 13 | 11 | 77 |
| T3 | Backend & Infrastructure | 13 | 10 | 10 | 5 | 11 | 11 | 10 | 13 | 83 |
| T4 | AI Detection | 6 | 8 | 5 | 5 | 10 | 8 | 8 | 8 | 58 |
| T5 | AI Forensics | 7 | 8 | 5 | 5 | 8 | 10 | 13 | 11 | 67 |
| T6 | Frontend / UX | 8 | 10 | 13 | 5 | 8 | 8 | 13 | 13 | 78 |
| T7 | Evaluation & Benchmarks | 8 | 11 | 8 | 8 | 8 | 10 | 13 | 13 | 79 |

Sprint 4 is short (8 working days), so everyone carries less. Each person plans about 10–13 points per sprint until real velocity is known.

!!! warning "Stretch work"
    42 points are labelled `stretch` and have no sprint: [KAN-107](https://pranav01.atlassian.net/browse/KAN-107), [KAN-114](https://pranav01.atlassian.net/browse/KAN-114), [KAN-115](https://pranav01.atlassian.net/browse/KAN-115), [KAN-122](https://pranav01.atlassian.net/browse/KAN-122), [KAN-123](https://pranav01.atlassian.net/browse/KAN-123), [KAN-124](https://pranav01.atlassian.net/browse/KAN-124), [KAN-125](https://pranav01.atlassian.net/browse/KAN-125), [KAN-128](https://pranav01.atlassian.net/browse/KAN-128), [KAN-130](https://pranav01.atlassian.net/browse/KAN-130). Pull one in only when the sprint goal is safe and the team agrees.

## Sprint 1

**2 Nov 2026 → 13 Nov 2026 · Definition & Architecture** · Milestone: **M0 Architecture freeze (13 Nov)**

| Key | Story | Owner | Tier | Pts | Due |
|---|---|---|---|---|---|
| [KAN-15](https://pranav01.atlassian.net/browse/KAN-15) | Run kickoff: problem, users, MVP, non-goals, roles | T1 | MVP | 2 | 13 Nov 2026 |
| [KAN-16](https://pranav01.atlassian.net/browse/KAN-16) | Set up Jira project, board, sprints and Confluence space | T1 | MVP | 2 | 13 Nov 2026 |
| [KAN-17](https://pranav01.atlassian.net/browse/KAN-17) | Write and approve ADR-001 to ADR-004 | T1 | MVP | 5 | 13 Nov 2026 |
| [KAN-18](https://pranav01.atlassian.net/browse/KAN-18) | Freeze trace/span/link contract and success-metric targets (M0) | T1 | MVP | 3 | 13 Nov 2026 |
| [KAN-19](https://pranav01.atlassian.net/browse/KAN-19) | Prototype SDK API shape including inputs_from links | T2 | MVP | 3 | 13 Nov 2026 |
| [KAN-20](https://pranav01.atlassian.net/browse/KAN-20) | Map span model to OpenTelemetry attributes | T2 | MVP | 3 | 13 Nov 2026 |
| [KAN-21](https://pranav01.atlassian.net/browse/KAN-21) | Create repository, branch protection, PR and issue templates | T3 | MVP | 2 | 13 Nov 2026 |
| [KAN-22](https://pranav01.atlassian.net/browse/KAN-22) | Docker Compose stack with PostgreSQL, Redis and MinIO | T3 | MVP | 3 | 13 Nov 2026 |
| [KAN-23](https://pranav01.atlassian.net/browse/KAN-23) | FastAPI skeleton with config, /health and /ready | T3 | MVP | 3 | 13 Nov 2026 |
| [KAN-24](https://pranav01.atlassian.net/browse/KAN-24) | CI pipeline: Ruff, mypy, pytest, frontend lint/type/test | T3 | MVP | 3 | 13 Nov 2026 |
| [KAN-25](https://pranav01.atlassian.net/browse/KAN-25) | Write ADR-005 (Celery) and ADR-006 (capture, retention, privacy) | T3 | MVP | 2 | 13 Nov 2026 |
| [KAN-26](https://pranav01.atlassian.net/browse/KAN-26) | Implement taxonomy module v1 with definitions | T4 | MVP | 3 | 13 Nov 2026 |
| [KAN-27](https://pranav01.atlassian.net/browse/KAN-27) | Investigate Jev access and DecisionGate options | T4 | Target | 3 | 13 Nov 2026 |
| [KAN-28](https://pranav01.atlassian.net/browse/KAN-28) | Write RCA algorithm design with hand-built fixture traces | T5 | MVP | 5 | 13 Nov 2026 |
| [KAN-29](https://pranav01.atlassian.net/browse/KAN-29) | Design evidence and claim data model | T5 | MVP | 2 | 13 Nov 2026 |
| [KAN-30](https://pranav01.atlassian.net/browse/KAN-30) | Scaffold Next.js console with Tailwind, ESLint, Prettier, Vitest | T6 | MVP | 3 | 13 Nov 2026 |
| [KAN-31](https://pranav01.atlassian.net/browse/KAN-31) | Wireframe Traces explorer and Failures investigation screens | T6 | MVP | 5 | 13 Nov 2026 |
| [KAN-32](https://pranav01.atlassian.net/browse/KAN-32) | Design benchmark suite and document benchmark | T7 | MVP | 3 | 13 Nov 2026 |
| [KAN-33](https://pranav01.atlassian.net/browse/KAN-33) | Draft evaluation protocol: metrics, dev/held-out split | T7 | MVP | 3 | 13 Nov 2026 |
| [KAN-34](https://pranav01.atlassian.net/browse/KAN-34) | Implement InjectedFault schema | T7 | MVP | 2 | 13 Nov 2026 |

## Sprint 2

**16 Nov 2026 → 27 Nov 2026 · SDK & Core Trace**

| Key | Story | Owner | Tier | Pts | Due |
|---|---|---|---|---|---|
| [KAN-35](https://pranav01.atlassian.net/browse/KAN-35) | Publish OpenAPI contract v1 with mock server | T1 | MVP | 5 | 27 Nov 2026 |
| [KAN-36](https://pranav01.atlassian.net/browse/KAN-36) | Run sprint 1 integration review | T1 | MVP | 2 | 27 Nov 2026 |
| [KAN-37](https://pranav01.atlassian.net/browse/KAN-37) | SDK core: Forensics client, @trace decorator, span context manager | T2 | MVP | 5 | 27 Nov 2026 |
| [KAN-38](https://pranav01.atlassian.net/browse/KAN-38) | SDK batching exporter with retry and background flush | T2 | MVP | 3 | 27 Nov 2026 |
| [KAN-39](https://pranav01.atlassian.net/browse/KAN-39) | POST /v1/ingest/batch: idempotent upsert of traces, spans and links | T2 | MVP | 5 | 27 Nov 2026 |
| [KAN-40](https://pranav01.atlassian.net/browse/KAN-40) | Database models and first migration: Project, ApiKey, Trace, Span, SpanLink | T3 | MVP | 5 | 27 Nov 2026 |
| [KAN-41](https://pranav01.atlassian.net/browse/KAN-41) | Project and API key endpoints with hashed keys | T3 | MVP | 5 | 27 Nov 2026 |
| [KAN-42](https://pranav01.atlassian.net/browse/KAN-42) | Rule validator framework and QualitySignal interface | T4 | MVP | 5 | 27 Nov 2026 |
| [KAN-43](https://pranav01.atlassian.net/browse/KAN-43) | Rules: JSON schema validity and tool error | T4 | MVP | 3 | 27 Nov 2026 |
| [KAN-44](https://pranav01.atlassian.net/browse/KAN-44) | Build data-flow graph from span links with parent/order fallback | T5 | MVP | 5 | 27 Nov 2026 |
| [KAN-45](https://pranav01.atlassian.net/browse/KAN-45) | Encode RCA fixture traces as automated tests | T5 | MVP | 3 | 27 Nov 2026 |
| [KAN-46](https://pranav01.atlassian.net/browse/KAN-46) | Console shell: navigation, session stub, typed API client from OpenAPI | T6 | MVP | 5 | 27 Nov 2026 |
| [KAN-47](https://pranav01.atlassian.net/browse/KAN-47) | Trace list page with filters against mock API | T6 | MVP | 5 | 27 Nov 2026 |
| [KAN-48](https://pranav01.atlassian.net/browse/KAN-48) | Document benchmark app (A) instrumented with the SDK | T7 | MVP | 8 | 27 Nov 2026 |
| [KAN-49](https://pranav01.atlassian.net/browse/KAN-49) | Document benchmark faults: hallucinated entity, omitted amount, schema violation | T7 | MVP | 3 | 27 Nov 2026 |

## Sprint 3

**30 Nov 2026 → 11 Dec 2026 · Trace Platform** · Milestone: **M1 Vertical slice (11 Dec)**

| Key | Story | Owner | Tier | Pts | Due |
|---|---|---|---|---|---|
| [KAN-50](https://pranav01.atlassian.net/browse/KAN-50) | Vertical slice integration and M1 demo (11 Dec) | T1 | MVP | 3 | 11 Dec 2026 |
| [KAN-51](https://pranav01.atlassian.net/browse/KAN-51) | Generate TypeScript types from OpenAPI in CI and fail on drift | T1 | MVP | 2 | 11 Dec 2026 |
| [KAN-52](https://pranav01.atlassian.net/browse/KAN-52) | Trace assembly on completion: derived totals, structure validation | T2 | MVP | 5 | 11 Dec 2026 |
| [KAN-53](https://pranav01.atlassian.net/browse/KAN-53) | SDK-side redaction of secrets and configured PII patterns | T2 | MVP | 3 | 11 Dec 2026 |
| [KAN-54](https://pranav01.atlassian.net/browse/KAN-54) | OpenAI adapter with automatic LLM spans | T2 | Target | 5 | 11 Dec 2026 |
| [KAN-55](https://pranav01.atlassian.net/browse/KAN-55) | Store large payloads in object storage by reference | T3 | MVP | 3 | 11 Dec 2026 |
| [KAN-56](https://pranav01.atlassian.net/browse/KAN-56) | Trace query API: list, filter, detail with spans and links | T3 | MVP | 5 | 11 Dec 2026 |
| [KAN-57](https://pranav01.atlassian.net/browse/KAN-57) | Seed script for demo project and sample traces | T3 | MVP | 2 | 11 Dec 2026 |
| [KAN-58](https://pranav01.atlassian.net/browse/KAN-58) | Rules: extracted value appears in source, citation exists | T4 | MVP | 5 | 11 Dec 2026 |
| [KAN-59](https://pranav01.atlassian.net/browse/KAN-59) | RCA v0: backward walk to earliest operational error | T5 | MVP | 5 | 11 Dec 2026 |
| [KAN-60](https://pranav01.atlassian.net/browse/KAN-60) | Trace explorer DAG with React Flow | T6 | MVP | 8 | 11 Dec 2026 |
| [KAN-61](https://pranav01.atlassian.net/browse/KAN-61) | Timeline view and span detail drawer | T6 | MVP | 5 | 11 Dec 2026 |
| [KAN-62](https://pranav01.atlassian.net/browse/KAN-62) | RAG benchmark app (B) v1 instrumented | T7 | MVP | 8 | 11 Dec 2026 |

## Sprint 4

**14 Dec 2026 → 23 Dec 2026 · AI Integrations & Detection base (short sprint)**

| Key | Story | Owner | Tier | Pts | Due |
|---|---|---|---|---|---|
| [KAN-63](https://pranav01.atlassian.net/browse/KAN-63) | Publish architecture overview and ADR index in Confluence | T1 | MVP | 2 | 23 Dec 2026 |
| [KAN-64](https://pranav01.atlassian.net/browse/KAN-64) | Token and cost calculation with pricing table | T2 | MVP | 3 | 23 Dec 2026 |
| [KAN-65](https://pranav01.atlassian.net/browse/KAN-65) | Version metadata: pipeline, prompt, component, git commit | T2 | MVP | 2 | 23 Dec 2026 |
| [KAN-66](https://pranav01.atlassian.net/browse/KAN-66) | Celery worker, AnalysisJob model and GET /v1/jobs/{id} | T3 | MVP | 5 | 23 Dec 2026 |
| [KAN-67](https://pranav01.atlassian.net/browse/KAN-67) | Detection pipeline runs on trace completion | T4 | MVP | 5 | 23 Dec 2026 |
| [KAN-68](https://pranav01.atlassian.net/browse/KAN-68) | Evidence store: create EvidenceRef from spans, documents and signals | T5 | MVP | 5 | 23 Dec 2026 |
| [KAN-69](https://pranav01.atlassian.net/browse/KAN-69) | Settings: project and API key management UI | T6 | MVP | 3 | 23 Dec 2026 |
| [KAN-70](https://pranav01.atlassian.net/browse/KAN-70) | Span payload viewer for object-store payloads | T6 | MVP | 2 | 23 Dec 2026 |
| [KAN-71](https://pranav01.atlassian.net/browse/KAN-71) | RAG faults: remove relevant doc, irrelevant docs, corrupt ranking, top-k cutoff | T7 | MVP | 5 | 23 Dec 2026 |
| [KAN-72](https://pranav01.atlassian.net/browse/KAN-72) | Write ADR-007 evaluation methodology | T7 | MVP | 3 | 23 Dec 2026 |

## Sprint 5

**4 Jan 2027 → 15 Jan 2027 · Detection**

| Key | Story | Owner | Tier | Pts | Due |
|---|---|---|---|---|---|
| [KAN-73](https://pranav01.atlassian.net/browse/KAN-73) | Post-holiday scope checkpoint toward M2 | T1 | MVP | 2 | 15 Jan 2027 |
| [KAN-74](https://pranav01.atlassian.net/browse/KAN-74) | Design candidate ranking score with T5 | T1 | Target | 3 | 15 Jan 2027 |
| [KAN-75](https://pranav01.atlassian.net/browse/KAN-75) | Helpers for retrieval and tool auto-instrumentation | T2 | Target | 5 | 15 Jan 2027 |
| [KAN-76](https://pranav01.atlassian.net/browse/KAN-76) | SDK quickstart guide | T2 | MVP | 3 | 15 Jan 2027 |
| [KAN-77](https://pranav01.atlassian.net/browse/KAN-77) | Flags endpoint and POST /v1/traces/{id}/analyses | T3 | MVP | 5 | 15 Jan 2027 |
| [KAN-78](https://pranav01.atlassian.net/browse/KAN-78) | Rate limits and request size limits | T3 | MVP | 3 | 15 Jan 2027 |
| [KAN-102](https://pranav01.atlassian.net/browse/KAN-102) | Platform metrics and correlation-id logging | T3 | MVP | 3 | 15 Jan 2027 |
| [KAN-79](https://pranav01.atlassian.net/browse/KAN-79) | Statistical checks: latency, cost and token anomalies | T4 | Target | 5 | 15 Jan 2027 |
| [KAN-80](https://pranav01.atlassian.net/browse/KAN-80) | LLM judge: answer faithfulness to evidence | T4 | MVP | 5 | 15 Jan 2027 |
| [KAN-81](https://pranav01.atlassian.net/browse/KAN-81) | RCA v1: backward traversal using quality deltas | T5 | MVP | 8 | 15 Jan 2027 |
| [KAN-82](https://pranav01.atlassian.net/browse/KAN-82) | Flag button and analysis progress UI | T6 | MVP | 3 | 15 Jan 2027 |
| [KAN-83](https://pranav01.atlassian.net/browse/KAN-83) | Failures list page | T6 | MVP | 5 | 15 Jan 2027 |
| [KAN-84](https://pranav01.atlassian.net/browse/KAN-84) | Agent benchmark app (C) v1 with planner and tools | T7 | Target | 8 | 15 Jan 2027 |

## Sprint 6

**18 Jan 2027 → 29 Jan 2027 · Forensics** · Milestone: **M2 MVP (29 Jan)**

| Key | Story | Owner | Tier | Pts | Due |
|---|---|---|---|---|---|
| [KAN-85](https://pranav01.atlassian.net/browse/KAN-85) | MVP end-to-end test and M2 demo (29 Jan) | T1 | MVP | 3 | 29 Jan 2027 |
| [KAN-86](https://pranav01.atlassian.net/browse/KAN-86) | Implement candidate ranking v1 with T5 | T1 | Target | 3 | 29 Jan 2027 |
| [KAN-87](https://pranav01.atlassian.net/browse/KAN-87) | SDK automatic linking by output object identity | T2 | Target | 5 | 29 Jan 2027 |
| [KAN-88](https://pranav01.atlassian.net/browse/KAN-88) | SDK/backend contract tests | T2 | MVP | 3 | 29 Jan 2027 |
| [KAN-89](https://pranav01.atlassian.net/browse/KAN-89) | Diagnosis and claim models with list/detail APIs | T3 | MVP | 5 | 29 Jan 2027 |
| [KAN-90](https://pranav01.atlassian.net/browse/KAN-90) | Audit log for key/config changes and overrides | T3 | Target | 3 | 29 Jan 2027 |
| [KAN-101](https://pranav01.atlassian.net/browse/KAN-101) | Datasets API (list/create, add cases) | T3 | MVP | 3 | 29 Jan 2027 |
| [KAN-91](https://pranav01.atlassian.net/browse/KAN-91) | DecisionGate interface and LLM classifier fallback backend | T4 | Target | 8 | 29 Jan 2027 |
| [KAN-92](https://pranav01.atlassian.net/browse/KAN-92) | Propagation labelling and span roles | T5 | Target | 5 | 29 Jan 2027 |
| [KAN-93](https://pranav01.atlassian.net/browse/KAN-93) | Explanation model: evidence-cited, injection-safe diagnosis text | T5 | MVP | 5 | 29 Jan 2027 |
| [KAN-94](https://pranav01.atlassian.net/browse/KAN-94) | Failure investigation page | T6 | MVP | 8 | 29 Jan 2027 |
| [KAN-95](https://pranav01.atlassian.net/browse/KAN-95) | Agent faults: wrong tool, malformed args, tool timeout, loop | T7 | Target | 5 | 29 Jan 2027 |
| [KAN-96](https://pranav01.atlassian.net/browse/KAN-96) | Accuracy harness on dev set: Top-1, Top-3, macro-F1 | T7 | MVP | 5 | 29 Jan 2027 |

## Sprint 7

**1 Feb 2027 → 12 Feb 2027 · Evidence, Review & Evaluation** · Milestone: **M3 Feature freeze (12 Feb)**

| Key | Story | Owner | Tier | Pts | Due |
|---|---|---|---|---|---|
| [KAN-97](https://pranav01.atlassian.net/browse/KAN-97) | Security review checkpoint | T1 | MVP | 2 | 12 Feb 2027 |
| [KAN-109](https://pranav01.atlassian.net/browse/KAN-109) | Feature freeze review and cut list (M3, 12 Feb) | T1 | Target | 2 | 12 Feb 2027 |
| [KAN-98](https://pranav01.atlassian.net/browse/KAN-98) | Trace compare backend: alignment and first divergence | T2 | Target | 5 | 12 Feb 2027 |
| [KAN-99](https://pranav01.atlassian.net/browse/KAN-99) | Server-side redaction safety net at ingestion | T2 | MVP | 3 | 12 Feb 2027 |
| [KAN-111](https://pranav01.atlassian.net/browse/KAN-111) | Analytics queries: failures by category, step, model, prompt | T2 | Target | 5 | 12 Feb 2027 |
| [KAN-100](https://pranav01.atlassian.net/browse/KAN-100) | Human feedback endpoint and eval case from confirmed diagnosis | T3 | MVP | 5 | 12 Feb 2027 |
| [KAN-113](https://pranav01.atlassian.net/browse/KAN-113) | Shared staging deployment with Caddy and auto-deploy | T3 | Target | 5 | 12 Feb 2027 |
| [KAN-103](https://pranav01.atlassian.net/browse/KAN-103) | Jev DecisionGate backend (if ADR-004 confirmed) with comparison logging | T4 | Target | 5 | 12 Feb 2027 |
| [KAN-104](https://pranav01.atlassian.net/browse/KAN-104) | Evidence sufficiency and human review gate decisions | T4 | Target | 3 | 12 Feb 2027 |
| [KAN-105](https://pranav01.atlassian.net/browse/KAN-105) | Grounding gate | T5 | MVP | 8 | 12 Feb 2027 |
| [KAN-116](https://pranav01.atlassian.net/browse/KAN-116) | Candidate ranking v2 with rationale | T5 | Target | 5 | 12 Feb 2027 |
| [KAN-106](https://pranav01.atlassian.net/browse/KAN-106) | Human feedback UI: confirm, correct, unsure | T6 | MVP | 5 | 12 Feb 2027 |
| [KAN-118](https://pranav01.atlassian.net/browse/KAN-118) | Evaluations UI: datasets, cases, run history | T6 | Target | 8 | 12 Feb 2027 |
| [KAN-108](https://pranav01.atlassian.net/browse/KAN-108) | Remaining faults for A/B/C and held-out split | T7 | MVP | 5 | 12 Feb 2027 |
| [KAN-119](https://pranav01.atlassian.net/browse/KAN-119) | Regression runner with baseline comparison | T7 | Target | 8 | 12 Feb 2027 |

## Sprint 8

**15 Feb 2027 → 26 Feb 2027 · Hardening, Report & Demo prep** · Milestone: **M4 Code complete / release candidate (26 Feb)**

| Key | Story | Owner | Tier | Pts | Due |
|---|---|---|---|---|---|
| [KAN-120](https://pranav01.atlassian.net/browse/KAN-120) | Code freeze gate (M4, 26 Feb) | T1 | Target | 2 | 26 Feb 2027 |
| [KAN-121](https://pranav01.atlassian.net/browse/KAN-121) | Draft final demo script | T1 | Target | 3 | 26 Feb 2027 |
| [KAN-132](https://pranav01.atlassian.net/browse/KAN-132) | Final demo rehearsals, release notes and live demo (early March) | T1 | MVP | 5 | 5 Mar 2027 |
| [KAN-110](https://pranav01.atlassian.net/browse/KAN-110) | Compare screen UI with T6 | T2 | Target | 5 | 26 Feb 2027 |
| [KAN-133](https://pranav01.atlassian.net/browse/KAN-133) | SDK guide and API reference polish | T2 | MVP | 3 | 26 Feb 2027 |
| [KAN-134](https://pranav01.atlassian.net/browse/KAN-134) | Bug fixing: SDK, ingestion, compare, analytics | T2 | MVP | 3 | 26 Feb 2027 |
| [KAN-112](https://pranav01.atlassian.net/browse/KAN-112) | Capture policy enforcement and retention job | T3 | MVP | 5 | 26 Feb 2027 |
| [KAN-135](https://pranav01.atlassian.net/browse/KAN-135) | Security tests: redaction, cross-project, oversized, prompt injection | T3 | MVP | 5 | 26 Feb 2027 |
| [KAN-136](https://pranav01.atlassian.net/browse/KAN-136) | Release candidate on staging with runbook (M4, 26 Feb) | T3 | MVP | 3 | 26 Feb 2027 |
| [KAN-126](https://pranav01.atlassian.net/browse/KAN-126) | Benchmark DecisionGate backends vs rules vs LLM judge | T4 | Target | 5 | 26 Feb 2027 |
| [KAN-137](https://pranav01.atlassian.net/browse/KAN-137) | Detection documentation and bug fixes | T4 | MVP | 3 | 26 Feb 2027 |
| [KAN-117](https://pranav01.atlassian.net/browse/KAN-117) | Tune RCA on dev set | T5 | MVP | 3 | 26 Feb 2027 |
| [KAN-127](https://pranav01.atlassian.net/browse/KAN-127) | Support held-out evaluation and fix RCA defects | T5 | MVP | 5 | 26 Feb 2027 |
| [KAN-138](https://pranav01.atlassian.net/browse/KAN-138) | Forensics documentation and bug fixes | T5 | MVP | 3 | 26 Feb 2027 |
| [KAN-129](https://pranav01.atlassian.net/browse/KAN-129) | Overview and Analytics dashboards | T6 | Target | 8 | 26 Feb 2027 |
| [KAN-139](https://pranav01.atlassian.net/browse/KAN-139) | Playwright E2E for main flow and UI polish | T6 | MVP | 5 | 26 Feb 2027 |
| [KAN-131](https://pranav01.atlassian.net/browse/KAN-131) | Held-out accuracy runs for final metrics | T7 | MVP | 5 | 26 Feb 2027 |
| [KAN-140](https://pranav01.atlassian.net/browse/KAN-140) | Final evaluation report | T7 | MVP | 8 | 26 Feb 2027 |
