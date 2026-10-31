# User Stories

Every story lives in Jira project **KAN** under one of 14 epics. Points use the Fibonacci scale. Acceptance criteria are copied from Jira; Jira is the source of truth.

| Tier | Stories | Points |
|---|---|---|
| MVP | 91 | 366 |
| Target | 26 | 127 |
| Stretch | 9 | 42 |

## Functional requirements

| ID | Requirement | Tier |
|---|---|---|
| FR-01 | Create projects and project-scoped API keys | MVP |
| FR-02 | Ingest traces and spans via authenticated, idempotent batch API | MVP |
| FR-03 | Parent/child spans and data-flow span links | MVP |
| FR-04 | Record prompts, model, tokens, cost (USD), latency, errors, versions | MVP |
| FR-05 | Represent LLM, retrieval, reranker, tool, agent, transform, guardrail and custom spans | MVP |
| FR-06 | Show traces as timeline and dependency graph | MVP |
| FR-07 | Run deterministic span validators | MVP |
| FR-08 | DecisionGate bounded classifications (Jev or LLM fallback) | Target |
| FR-09 | At least one semantic LLM judge (more judges are Stretch) | MVP |
| FR-10 | Accept user flags for bad outputs | MVP |
| FR-11 | Root-cause localization on failed or flagged traces | MVP |
| FR-12 | Ranked candidates and propagation paths | Target |
| FR-13 | Evidence-backed diagnoses with confidence | MVP |
| FR-14 | Ground claims against stored evidence | MVP |
| FR-15 | Human confirm / correct / unsure | MVP |
| FR-16 | Eval cases from confirmed failures | MVP |
| FR-17 | Re-run eval datasets against a version and compare with baseline | Target |
| FR-18 | Experiments comparing versions | Stretch |
| FR-19 | Quality, failure, cost and latency analytics | Target |
| FR-20 | Controlled fault injection in benchmark apps | MVP |
| FR-21 | Export diagnoses and results (JSON/CSV) | Stretch |
| FR-22 | Health, readiness and service metrics | MVP |

!!! note "Changed for the 8-sprint plan"
    FR-18 (experiments) and FR-21 (export) moved from Target to Stretch so the build finishes by 26 Feb 2027.

## Project setup & architecture ([KAN-1](https://pranav01.atlassian.net/browse/KAN-1))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-15](https://pranav01.atlassian.net/browse/KAN-15) | Run kickoff: problem, users, MVP, non-goals, roles | T1 | 1 | MVP | 2 | Everyone has read Blueprint v1.1 and Errata<br>Role table agreed and names filled in Confluence<br>Working agreement (ceremonies, hours, channels) published |
| [KAN-16](https://pranav01.atlassian.net/browse/KAN-16) | Set up Jira project, board, sprints and Confluence space | T1 | 1 | MVP | 2 | Jira backlog imported from CSV<br>10 sprints created with dates<br>Confluence pages published<br>GitHub for Jira app connected |
| [KAN-17](https://pranav01.atlassian.net/browse/KAN-17) | Write and approve ADR-001 to ADR-004 | T1 | 1 | MVP | 5 | ADR-001 modular monolith<br>ADR-002 Postgres + object store<br>ADR-003 OTel compatibility and span links<br>ADR-004 DecisionGate boundary and Jev backend decision<br>Each ADR approved by 2 reviewers |
| [KAN-18](https://pranav01.atlassian.net/browse/KAN-18) | Freeze trace/span/link contract and success-metric targets (M0) | T1 | 1 | MVP | 3 | Pydantic models for Trace, Span, SpanLink merged<br>Metric targets in §2.5 confirmed or changed<br>MVP scope frozen on 13 Nov |
| [KAN-35](https://pranav01.atlassian.net/browse/KAN-35) | Publish OpenAPI contract v1 with mock server | T1 | 2 | MVP | 5 | All MVP endpoints from §13 described<br>Mock server used by frontend<br>Contract tests scaffolded |
| [KAN-36](https://pranav01.atlassian.net/browse/KAN-36) | Run sprint 1 integration review | T1 | 2 | MVP | 2 | Demo of SDK to ingestion path<br>Blocking issues logged in Jira |
| [KAN-50](https://pranav01.atlassian.net/browse/KAN-50) | Vertical slice integration and M1 demo (11 Dec) | T1 | 3 | MVP | 3 | Benchmark -> SDK -> ingestion -> storage -> trace UI works on a clean clone<br>Every member runs it locally<br>Recorded demo in Confluence |
| [KAN-51](https://pranav01.atlassian.net/browse/KAN-51) | Generate TypeScript types from OpenAPI in CI and fail on drift | T1 | 3 | MVP | 2 | CI fails if generated types differ from committed ones |
| [KAN-63](https://pranav01.atlassian.net/browse/KAN-63) | Publish architecture overview and ADR index in Confluence | T1 | 4 | MVP | 2 | Pages linked from space home<br>Diagrams match the 7 layers |
| [KAN-73](https://pranav01.atlassian.net/browse/KAN-73) | Post-holiday scope checkpoint toward M2 | T1 | 5 | MVP | 2 | Burn-down reviewed<br>Any MVP item at risk re-planned or cut with team agreement |
| [KAN-109](https://pranav01.atlassian.net/browse/KAN-109) | Feature freeze review and cut list (M3, 12 Feb) | T1 | 7 | Target | 2 | Remaining Target items triaged<br>Cut list agreed |
| [KAN-120](https://pranav01.atlassian.net/browse/KAN-120) | Code freeze gate (M4, 26 Feb) | T1 | 8 | Target | 2 | Only bug fixes after freeze<br>Open features moved to Stretch |

## Python SDK ([KAN-2](https://pranav01.atlassian.net/browse/KAN-2))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-19](https://pranav01.atlassian.net/browse/KAN-19) | Prototype SDK API shape including inputs_from links | T2 | 1 | MVP | 3 | Spike branch shows decorator, span context manager and inputs_from<br>Example from §7.2 runs against a stub exporter<br>Reviewed by T1 and T5 |
| [KAN-20](https://pranav01.atlassian.net/browse/KAN-20) | Map span model to OpenTelemetry attributes | T2 | 1 | MVP | 3 | Mapping table for IDs, span kinds, links and gen_ai attributes in Confluence<br>Gaps listed |
| [KAN-37](https://pranav01.atlassian.net/browse/KAN-37) | SDK core: Forensics client, @trace decorator, span context manager | T2 | 2 | MVP | 5 | Nested spans get correct parent<br>inputs_from creates SpanLink<br>Exceptions recorded as status=error<br>Unit tests >= 85% coverage |
| [KAN-38](https://pranav01.atlassian.net/browse/KAN-38) | SDK batching exporter with retry and background flush | T2 | 2 | MVP | 3 | Batches up to 100 spans or 1 s<br>Retries 3 times with backoff<br>Never raises into user code |
| [KAN-53](https://pranav01.atlassian.net/browse/KAN-53) | SDK-side redaction of secrets and configured PII patterns | T2 | 3 | MVP | 3 | Authorization headers, cookies, API keys, passwords redacted<br>Custom regex patterns from config<br>Tests prove secrets never leave the process |
| [KAN-54](https://pranav01.atlassian.net/browse/KAN-54) | OpenAI adapter with automatic LLM spans | T2 | 3 | Target | 5 | Chat completion calls produce LLM spans with model, tokens, latency<br>Streaming supported<br>Works with recorded fixtures (no live key in CI) |
| [KAN-75](https://pranav01.atlassian.net/browse/KAN-75) | Helpers for retrieval and tool auto-instrumentation | T2 | 5 | Target | 5 | Decorators for retriever and tool functions<br>Documents/tool args captured per capture policy |
| [KAN-76](https://pranav01.atlassian.net/browse/KAN-76) | SDK quickstart guide | T2 | 5 | MVP | 3 | Install, configure, first trace in under 10 minutes<br>Published in repo and Confluence |
| [KAN-87](https://pranav01.atlassian.net/browse/KAN-87) | SDK automatic linking by output object identity | T2 | 6 | Target | 5 | Passing a previous span's output into a new span creates a link<br>Opt-out flag<br>Tests for false links |

## Ingestion & trace platform ([KAN-3](https://pranav01.atlassian.net/browse/KAN-3))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-39](https://pranav01.atlassian.net/browse/KAN-39) | POST /v1/ingest/batch: idempotent upsert of traces, spans and links | T2 | 2 | MVP | 5 | Same batch twice creates no duplicates<br>Spans before trace accepted<br>Invalid payload returns 422 with details<br>p95 < 200 ms for 100 spans locally |
| [KAN-52](https://pranav01.atlassian.net/browse/KAN-52) | Trace assembly on completion: derived totals, structure validation | T2 | 3 | MVP | 5 | Total latency, tokens, cost computed<br>Missing parents flagged<br>status=incomplete after timeout |
| [KAN-64](https://pranav01.atlassian.net/browse/KAN-64) | Token and cost calculation with pricing table | T2 | 4 | MVP | 3 | Cost in USD Decimal(12,6)<br>Pricing table versioned in config<br>Totals roll up to trace |
| [KAN-65](https://pranav01.atlassian.net/browse/KAN-65) | Version metadata: pipeline, prompt, component, git commit | T2 | 4 | MVP | 2 | Fields captured by SDK and filterable in API |
| [KAN-88](https://pranav01.atlassian.net/browse/KAN-88) | SDK/backend contract tests | T2 | 6 | MVP | 3 | CI fails when SDK payload and API schema diverge |

## Data model, product APIs & jobs ([KAN-4](https://pranav01.atlassian.net/browse/KAN-4))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-23](https://pranav01.atlassian.net/browse/KAN-23) | FastAPI skeleton with config, /health and /ready | T3 | 1 | MVP | 3 | /ready checks DB, Redis and MinIO<br>Settings via pydantic-settings<br>Structured JSON logging |
| [KAN-25](https://pranav01.atlassian.net/browse/KAN-25) | Write ADR-005 (Celery) and ADR-006 (capture, retention, privacy) | T3 | 1 | MVP | 2 | Both ADRs approved<br>Capture modes and retention defaults decided |
| [KAN-40](https://pranav01.atlassian.net/browse/KAN-40) | Database models and first migration: Project, ApiKey, Trace, Span, SpanLink | T3 | 2 | MVP | 5 | Alembic upgrade/downgrade works<br>Indexes on project_id, trace_id, started_at<br>Testcontainers integration test |
| [KAN-55](https://pranav01.atlassian.net/browse/KAN-55) | Store large payloads in object storage by reference | T3 | 3 | MVP | 3 | Payloads > 8 KB go to MinIO<br>input_ref/output_ref resolve via API<br>Lifecycle tested |
| [KAN-56](https://pranav01.atlassian.net/browse/KAN-56) | Trace query API: list, filter, detail with spans and links | T3 | 3 | MVP | 5 | GET /v1/traces and /v1/traces/{id} match OpenAPI<br>Detail returns spans, links, signals<br>Query p95 < 300 ms for 10k traces |
| [KAN-57](https://pranav01.atlassian.net/browse/KAN-57) | Seed script for demo project and sample traces | T3 | 3 | MVP | 2 | make seed creates project, key and 50 traces |
| [KAN-66](https://pranav01.atlassian.net/browse/KAN-66) | Celery worker, AnalysisJob model and GET /v1/jobs/{id} | T3 | 4 | MVP | 5 | Job states queued/running/succeeded/failed/cancelled<br>Progress and stage updated<br>Idempotent by job id<br>Retries with backoff |
| [KAN-89](https://pranav01.atlassian.net/browse/KAN-89) | Diagnosis and claim models with list/detail APIs | T3 | 6 | MVP | 5 | GET /v1/diagnoses and /v1/diagnoses/{id} return claims, evidence, roles<br>Migration tested |
| [KAN-124](https://pranav01.atlassian.net/browse/KAN-124) | Server-Sent Events for job progress | T3 | Stretch | Stretch | 3 | SSE endpoint<br>frontend falls back to polling |

## Security, DevOps & platform observability ([KAN-5](https://pranav01.atlassian.net/browse/KAN-5))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-21](https://pranav01.atlassian.net/browse/KAN-21) | Create repository, branch protection, PR and issue templates | T3 | 1 | MVP | 2 | main protected, 1 approval and CI required<br>PR template asks for Jira key and tests<br>CODEOWNERS skeleton |
| [KAN-22](https://pranav01.atlassian.net/browse/KAN-22) | Docker Compose stack with PostgreSQL, Redis and MinIO | T3 | 1 | MVP | 3 | docker compose up starts all three with healthchecks<br>.env.example documents variables<br>README quickstart |
| [KAN-24](https://pranav01.atlassian.net/browse/KAN-24) | CI pipeline: Ruff, mypy, pytest, frontend lint/type/test | T3 | 1 | MVP | 3 | Runs on every PR in under 10 min<br>Fails on lint or type errors<br>Status required for merge |
| [KAN-41](https://pranav01.atlassian.net/browse/KAN-41) | Project and API key endpoints with hashed keys | T3 | 2 | MVP | 5 | Key shown once, stored as argon2 hash<br>Revocation blocks ingestion within 1 min<br>Cross-project access returns 404 |
| [KAN-78](https://pranav01.atlassian.net/browse/KAN-78) | Rate limits and request size limits | T3 | 5 | MVP | 3 | Ingestion and analysis endpoints limited per key<br>413 on oversized payloads<br>Tests |
| [KAN-90](https://pranav01.atlassian.net/browse/KAN-90) | Audit log for key/config changes and overrides | T3 | 6 | Target | 3 | Entries written for key create/revoke, capture policy change, human corrections |
| [KAN-97](https://pranav01.atlassian.net/browse/KAN-97) | Security review checkpoint | T1 | 7 | MVP | 2 | Threat review against §17<br>Issues logged with owners |
| [KAN-99](https://pranav01.atlassian.net/browse/KAN-99) | Server-side redaction safety net at ingestion | T2 | 7 | MVP | 3 | Same patterns as SDK applied again<br>Metric counts redactions |
| [KAN-102](https://pranav01.atlassian.net/browse/KAN-102) | Platform metrics and correlation-id logging | T3 | 5 | MVP | 3 | Metrics from §18 exposed<br>Logs carry trace/job ids |
| [KAN-112](https://pranav01.atlassian.net/browse/KAN-112) | Capture policy enforcement and retention job | T3 | 8 | MVP | 5 | metadata-only/sampled/full enforced at ingestion<br>Nightly retention deletes rows and objects |
| [KAN-113](https://pranav01.atlassian.net/browse/KAN-113) | Shared staging deployment with Caddy and auto-deploy | T3 | 7 | Target | 5 | Deploys from main after CI<br>TLS<br>Separate staging keys<br>Runbook |

## Detection & DecisionGate ([KAN-6](https://pranav01.atlassian.net/browse/KAN-6))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-26](https://pranav01.atlassian.net/browse/KAN-26) | Implement taxonomy module v1 with definitions | T4 | 1 | MVP | 3 | taxonomy.py with families and categories from §9<br>One-line definition per category<br>TS enum generated for frontend |
| [KAN-27](https://pranav01.atlassian.net/browse/KAN-27) | Investigate Jev access and DecisionGate options | T4 | 1 | Target | 3 | Document what Jev is, API, cost, latency<br>Recommendation for ADR-004<br>Fallback LLM classifier prompt sketched |
| [KAN-42](https://pranav01.atlassian.net/browse/KAN-42) | Rule validator framework and QualitySignal interface | T4 | 2 | MVP | 5 | Validators registered by span type<br>Each produces QualitySignal with evidence_ids<br>Crashing validator produces EVALUATOR_FAILURE signal, not a failed trace |
| [KAN-43](https://pranav01.atlassian.net/browse/KAN-43) | Rules: JSON schema validity and tool error | T4 | 2 | MVP | 3 | Schema rule on transform and LLM spans<br>Tool error rule on tool spans<br>Unit tests with fixtures |
| [KAN-58](https://pranav01.atlassian.net/browse/KAN-58) | Rules: extracted value appears in source, citation exists | T4 | 3 | MVP | 5 | Applied to document and RAG spans<br>Evidence points to source excerpt<br>Precision checked on fixtures |
| [KAN-67](https://pranav01.atlassian.net/browse/KAN-67) | Detection pipeline runs on trace completion | T4 | 4 | MVP | 5 | Runs all registered detectors in a worker<br>Signals persisted<br>One failing detector does not stop others |
| [KAN-79](https://pranav01.atlassian.net/browse/KAN-79) | Statistical checks: latency, cost and token anomalies | T4 | 5 | Target | 5 | Baseline per component_key with >= 30 traces<br>Z-score or IQR rule<br>Trace-level signals allowed (span_id null) |
| [KAN-80](https://pranav01.atlassian.net/browse/KAN-80) | LLM judge: answer faithfulness to evidence | T4 | 5 | MVP | 5 | Judge prompt separates evidence from instructions<br>Returns verdict, score, confidence<br>Cached by input hash |
| [KAN-91](https://pranav01.atlassian.net/browse/KAN-91) | DecisionGate interface and LLM classifier fallback backend | T4 | 6 | Target | 8 | Decisions: span health, family then category<br>Structured output validated<br>Backend name logged per decision |
| [KAN-103](https://pranav01.atlassian.net/browse/KAN-103) | Jev DecisionGate backend (if ADR-004 confirmed) with comparison logging | T4 | 7 | Target | 5 | Jev backend behind same interface<br>Toggle per project<br>If Jev unavailable, story closed as Won't Do with note |
| [KAN-104](https://pranav01.atlassian.net/browse/KAN-104) | Evidence sufficiency and human review gate decisions | T4 | 7 | Target | 3 | SUFFICIENT/MORE_EVIDENCE/UNDIAGNOSABLE<br>AUTO_ACCEPT/REVIEW_REQUIRED |
| [KAN-114](https://pranav01.atlassian.net/browse/KAN-114) | Additional judges: instruction following and citation support | T4 | Stretch | Stretch | 5 | Two more judges with fixtures and agreement check vs human labels |
| [KAN-115](https://pranav01.atlassian.net/browse/KAN-115) | Offline tool-call assessment decision | T4 | Stretch | Stretch | 3 | VALID/INVALID_ARGUMENTS/WRONG_TOOL/REVIEW on agent traces |
| [KAN-126](https://pranav01.atlassian.net/browse/KAN-126) | Benchmark DecisionGate backends vs rules vs LLM judge | T4 | 8 | Target | 5 | Accuracy, latency, cost per backend on dev set<br>Findings for report |

## Root-cause forensics ([KAN-7](https://pranav01.atlassian.net/browse/KAN-7))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-28](https://pranav01.atlassian.net/browse/KAN-28) | Write RCA algorithm design with hand-built fixture traces | T5 | 1 | MVP | 5 | Design doc in Confluence covering §10.1<br>At least 6 fixture traces (doc, RAG) with expected root cause<br>Reviewed by T1 |
| [KAN-44](https://pranav01.atlassian.net/browse/KAN-44) | Build data-flow graph from span links with parent/order fallback | T5 | 2 | MVP | 5 | Graph built from links<br>Fallback edges marked low-confidence<br>Cycles detected and reported |
| [KAN-45](https://pranav01.atlassian.net/browse/KAN-45) | Encode RCA fixture traces as automated tests | T5 | 2 | MVP | 3 | Fixtures from S0 load as traces<br>Expected root cause asserted (tests may be xfail until RCA lands) |
| [KAN-59](https://pranav01.atlassian.net/browse/KAN-59) | RCA v0: backward walk to earliest operational error | T5 | 3 | MVP | 5 | Returns earliest error span on fixtures with explicit errors<br>Unit tests pass |
| [KAN-74](https://pranav01.atlassian.net/browse/KAN-74) | Design candidate ranking score with T5 | T1 | 5 | Target | 3 | Score = severity x confidence x earliness documented<br>Tested on fixtures |
| [KAN-81](https://pranav01.atlassian.net/browse/KAN-81) | RCA v1: backward traversal using quality deltas | T5 | 5 | MVP | 8 | Uses signals on inputs vs outputs<br>Finds earliest significant degradation<br>Passes >= 70% of dev fixtures |
| [KAN-86](https://pranav01.atlassian.net/browse/KAN-86) | Implement candidate ranking v1 with T5 | T1 | 6 | Target | 3 | Top-3 candidates with scores returned<br>Unit tests |
| [KAN-92](https://pranav01.atlassian.net/browse/KAN-92) | Propagation labelling and span roles | T5 | 6 | Target | 5 | span_roles filled (root_cause, propagated, degraded, failed_output)<br>propagation_path stored |
| [KAN-116](https://pranav01.atlassian.net/browse/KAN-116) | Candidate ranking v2 with rationale | T5 | 7 | Target | 5 | Top-3 with rationale referencing evidence<br>Top-3 accuracy measured on dev |
| [KAN-117](https://pranav01.atlassian.net/browse/KAN-117) | Tune RCA on dev set | T5 | 8 | MVP | 3 | Dev Top-1 improved vs S5 baseline<br>No held-out data used |

## Evidence, explanation & grounding ([KAN-8](https://pranav01.atlassian.net/browse/KAN-8))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-29](https://pranav01.atlassian.net/browse/KAN-29) | Design evidence and claim data model | T5 | 1 | MVP | 2 | EvidenceRef and DiagnosisClaim fields agreed<br>Examples for each source_type |
| [KAN-68](https://pranav01.atlassian.net/browse/KAN-68) | Evidence store: create EvidenceRef from spans, documents and signals | T5 | 4 | MVP | 5 | content_hash computed<br>Lookup by trace and span<br>Unit tests |
| [KAN-93](https://pranav01.atlassian.net/browse/KAN-93) | Explanation model: evidence-cited, injection-safe diagnosis text | T5 | 6 | MVP | 5 | Prompt cites evidence IDs only<br>Traced content wrapped as untrusted data<br>Pre-gate text stored |
| [KAN-105](https://pranav01.atlassian.net/browse/KAN-105) | Grounding gate | T5 | 7 | MVP | 8 | Diagnosis split into claims<br>IDs, numbers and quotes verified<br>Unsupported claims removed and confidence lowered<br>Pre/post persisted<br>grounded flag set |

## Human review & eval cases ([KAN-9](https://pranav01.atlassian.net/browse/KAN-9))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-77](https://pranav01.atlassian.net/browse/KAN-77) | Flags endpoint and POST /v1/traces/{id}/analyses | T3 | 5 | MVP | 5 | Flag stored with reason/source<br>Analysis creates job and returns id<br>Flagging can auto-start analysis (config) |
| [KAN-100](https://pranav01.atlassian.net/browse/KAN-100) | Human feedback endpoint and eval case from confirmed diagnosis | T3 | 7 | MVP | 5 | Confirm/correct/unsure stored<br>Confirm or correct creates EvalCase with expected component<br>Audit entry written |
| [KAN-101](https://pranav01.atlassian.net/browse/KAN-101) | Datasets API (list/create, add cases) | T3 | 6 | MVP | 3 | GET/POST /v1/datasets<br>Dataset versioning |

## Benchmarks & fault injection ([KAN-10](https://pranav01.atlassian.net/browse/KAN-10))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-32](https://pranav01.atlassian.net/browse/KAN-32) | Design benchmark suite and document benchmark | T7 | 1 | MVP | 3 | Pipeline steps and component keys defined for A, B, C<br>Document dataset source chosen (synthetic/no PII) |
| [KAN-34](https://pranav01.atlassian.net/browse/KAN-34) | Implement InjectedFault schema | T7 | 1 | MVP | 2 | Pydantic model from §15.4<br>Serialized fixtures load in tests |
| [KAN-48](https://pranav01.atlassian.net/browse/KAN-48) | Document benchmark app (A) instrumented with the SDK | T7 | 2 | MVP | 8 | Extraction, classification, summarization spans with component keys<br>Runs from one command<br>Traces appear via ingestion |
| [KAN-49](https://pranav01.atlassian.net/browse/KAN-49) | Document benchmark faults: hallucinated entity, omitted amount, schema violation | T7 | 2 | MVP | 3 | Each fault reproducible by seed<br>InjectedFault record written with expected root cause |
| [KAN-62](https://pranav01.atlassian.net/browse/KAN-62) | RAG benchmark app (B) v1 instrumented | T7 | 3 | MVP | 8 | Query rewrite, retrieval, reranker, context build, LLM spans with links<br>Small local corpus<br>Answer correctness checker |
| [KAN-71](https://pranav01.atlassian.net/browse/KAN-71) | RAG faults: remove relevant doc, irrelevant docs, corrupt ranking, top-k cutoff | T7 | 4 | MVP | 5 | Each reproducible by seed<br>Expected root cause component recorded |
| [KAN-84](https://pranav01.atlassian.net/browse/KAN-84) | Agent benchmark app (C) v1 with planner and tools | T7 | 5 | Target | 8 | Planner, tool selection, tool call, observation, reasoning spans<br>3+ tools (calculator, search stub, DB stub) |
| [KAN-95](https://pranav01.atlassian.net/browse/KAN-95) | Agent faults: wrong tool, malformed args, tool timeout, loop | T7 | 6 | Target | 5 | Each reproducible by seed<br>Expected root cause recorded |
| [KAN-108](https://pranav01.atlassian.net/browse/KAN-108) | Remaining faults for A/B/C and held-out split | T7 | 7 | MVP | 5 | All faults in §15 implemented or explicitly cut<br>Held-out split frozen and not used for tuning |

## Evaluation, regression & experiments ([KAN-11](https://pranav01.atlassian.net/browse/KAN-11))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-33](https://pranav01.atlassian.net/browse/KAN-33) | Draft evaluation protocol: metrics, dev/held-out split | T7 | 1 | MVP | 3 | Metric definitions match §2.5<br>Split rule by fault type and seed<br>Input to ADR-007 |
| [KAN-72](https://pranav01.atlassian.net/browse/KAN-72) | Write ADR-007 evaluation methodology | T7 | 4 | MVP | 3 | Approved by T1, T4, T5<br>Defines dev/held-out, metrics and reporting |
| [KAN-96](https://pranav01.atlassian.net/browse/KAN-96) | Accuracy harness on dev set: Top-1, Top-3, macro-F1 | T7 | 6 | MVP | 5 | One command runs all dev faults and prints metrics<br>Results stored for trend |
| [KAN-119](https://pranav01.atlassian.net/browse/KAN-119) | Regression runner with baseline comparison | T7 | 7 | Target | 8 | POST /v1/eval-runs executes cases in isolation<br>Stores pass/fail, deltas, new failures<br>Advisory recommendation |
| [KAN-127](https://pranav01.atlassian.net/browse/KAN-127) | Support held-out evaluation and fix RCA defects | T5 | 8 | MVP | 5 | Held-out run completed once<br>Defects triaged |
| [KAN-130](https://pranav01.atlassian.net/browse/KAN-130) | Experiment engine across prompt/model/retriever variants | T7 | Stretch | Stretch | 8 | Runs variants on a dataset<br>Stores comparable metrics |
| [KAN-131](https://pranav01.atlassian.net/browse/KAN-131) | Held-out accuracy runs for final metrics | T7 | 8 | MVP | 5 | Top-1, Top-3, macro-F1, grounding, FPR, latency reported vs targets |
| [KAN-140](https://pranav01.atlassian.net/browse/KAN-140) | Final evaluation report | T7 | 8 | MVP | 8 | Methodology, results vs targets, error analysis, limitations<br>Reviewed by T1, T5 |

## Developer console ([KAN-12](https://pranav01.atlassian.net/browse/KAN-12))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-30](https://pranav01.atlassian.net/browse/KAN-30) | Scaffold Next.js console with Tailwind, ESLint, Prettier, Vitest | T6 | 1 | MVP | 3 | App builds in CI<br>Strict TS<br>Base layout and theme tokens |
| [KAN-31](https://pranav01.atlassian.net/browse/KAN-31) | Wireframe Traces explorer and Failures investigation screens | T6 | 1 | MVP | 5 | Low-fi wireframes in Confluence<br>Reviewed with T1, T5<br>Loading/empty/error states shown |
| [KAN-46](https://pranav01.atlassian.net/browse/KAN-46) | Console shell: navigation, session stub, typed API client from OpenAPI | T6 | 2 | MVP | 5 | All 9 nav entries present (stubs allowed)<br>API client generated in CI |
| [KAN-47](https://pranav01.atlassian.net/browse/KAN-47) | Trace list page with filters against mock API | T6 | 2 | MVP | 5 | Filter by status, health, pipeline_version, date<br>Pagination<br>Loading/empty/error states |
| [KAN-60](https://pranav01.atlassian.net/browse/KAN-60) | Trace explorer DAG with React Flow | T6 | 3 | MVP | 8 | Nodes coloured by status/health<br>Edges show parent and data-flow links<br>Handles 200+ spans smoothly |
| [KAN-61](https://pranav01.atlassian.net/browse/KAN-61) | Timeline view and span detail drawer | T6 | 3 | MVP | 5 | Gantt-style timeline<br>Drawer shows input/output, model, tokens, cost, errors |
| [KAN-69](https://pranav01.atlassian.net/browse/KAN-69) | Settings: project and API key management UI | T6 | 4 | MVP | 3 | Create project, create/revoke key, key shown once |
| [KAN-70](https://pranav01.atlassian.net/browse/KAN-70) | Span payload viewer for object-store payloads | T6 | 4 | MVP | 2 | Lazy-loads large payloads<br>JSON pretty view<br>Redacted fields marked |
| [KAN-82](https://pranav01.atlassian.net/browse/KAN-82) | Flag button and analysis progress UI | T6 | 5 | MVP | 3 | Flag from trace page<br>Polling every 2 s shows stage/progress<br>Error state on failed job |
| [KAN-83](https://pranav01.atlassian.net/browse/KAN-83) | Failures list page | T6 | 5 | MVP | 5 | Lists diagnoses with category, confidence, status<br>Filters<br>Links to investigation |
| [KAN-94](https://pranav01.atlassian.net/browse/KAN-94) | Failure investigation page | T6 | 6 | MVP | 8 | Root cause, category, confidence, roles colouring on DAG, evidence list<br>Matches §16 hero interaction |
| [KAN-106](https://pranav01.atlassian.net/browse/KAN-106) | Human feedback UI: confirm, correct, unsure | T6 | 7 | MVP | 5 | Correct lets reviewer pick span and category<br>Success creates eval case link |
| [KAN-107](https://pranav01.atlassian.net/browse/KAN-107) | Evidence timeline component | T6 | Stretch | Stretch | 5 | Evidence ordered by time with source type<br>Click jumps to span |
| [KAN-118](https://pranav01.atlassian.net/browse/KAN-118) | Evaluations UI: datasets, cases, run history | T6 | 7 | Target | 8 | Dataset and case browsing<br>Run list with pass/fail and delta vs baseline |
| [KAN-128](https://pranav01.atlassian.net/browse/KAN-128) | Experiments UI | T6 | Stretch | Stretch | 5 | Create experiment from dataset and variants<br>Compare quality/cost/latency |
| [KAN-129](https://pranav01.atlassian.net/browse/KAN-129) | Overview and Analytics dashboards | T6 | 8 | Target | 8 | KPIs, failures over time, top categories, cost/latency, override rate |

## Analytics, compare & export ([KAN-13](https://pranav01.atlassian.net/browse/KAN-13))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-98](https://pranav01.atlassian.net/browse/KAN-98) | Trace compare backend: alignment and first divergence | T2 | 7 | Target | 5 | Aligns spans by component_key<br>Returns first diverging span and field diffs |
| [KAN-110](https://pranav01.atlassian.net/browse/KAN-110) | Compare screen UI with T6 | T2 | 8 | Target | 5 | Side-by-side healthy vs failed traces<br>First divergence highlighted |
| [KAN-111](https://pranav01.atlassian.net/browse/KAN-111) | Analytics queries: failures by category, step, model, prompt | T2 | 7 | Target | 5 | Materialized or cached queries<br>Response < 500 ms |
| [KAN-122](https://pranav01.atlassian.net/browse/KAN-122) | Analytics overview API | T2 | Stretch | Stretch | 5 | GET /v1/analytics/overview returns KPIs for Overview screen |
| [KAN-123](https://pranav01.atlassian.net/browse/KAN-123) | Export diagnoses and benchmark results | T2 | Stretch | Stretch | 3 | POST /v1/exports JSON/CSV as a job<br>Download link |

## Hardening, documentation & final demo ([KAN-14](https://pranav01.atlassian.net/browse/KAN-14))

| Key | Story | Owner | Sprint | Tier | Pts | Acceptance criteria |
|---|---|---|---|---|---|---|
| [KAN-85](https://pranav01.atlassian.net/browse/KAN-85) | MVP end-to-end test and M2 demo (29 Jan) | T1 | 6 | MVP | 3 | Flag -> analyze -> diagnosis with evidence works on doc and RAG<br>E2E test in CI<br>Demo recorded |
| [KAN-121](https://pranav01.atlassian.net/browse/KAN-121) | Draft final demo script | T1 | 8 | Target | 3 | Follows §28<br>Fallback recordings for each step |
| [KAN-125](https://pranav01.atlassian.net/browse/KAN-125) | Load and performance tests | T3 | Stretch | Stretch | 5 | Burst ingestion, 500-span traces, 10 concurrent analyses<br>Results in Confluence |
| [KAN-132](https://pranav01.atlassian.net/browse/KAN-132) | Final demo rehearsals, release notes and live demo (early March) | T1 | 8 | MVP | 5 | Two full rehearsals<br>Release tagged<br>Final demo delivered<br>Retrospective held |
| [KAN-133](https://pranav01.atlassian.net/browse/KAN-133) | SDK guide and API reference polish | T2 | 8 | MVP | 3 | SDK guide complete<br>OpenAPI docs published |
| [KAN-134](https://pranav01.atlassian.net/browse/KAN-134) | Bug fixing: SDK, ingestion, compare, analytics | T2 | 8 | MVP | 3 | No open Highest/High bugs in owned areas |
| [KAN-135](https://pranav01.atlassian.net/browse/KAN-135) | Security tests: redaction, cross-project, oversized, prompt injection | T3 | 8 | MVP | 5 | All tests from §20 security row automated<br>No critical findings open |
| [KAN-136](https://pranav01.atlassian.net/browse/KAN-136) | Release candidate on staging with runbook (M4, 26 Feb) | T3 | 8 | MVP | 3 | RC deployed<br>Rollback tested<br>Runbook in Confluence |
| [KAN-137](https://pranav01.atlassian.net/browse/KAN-137) | Detection documentation and bug fixes | T4 | 8 | MVP | 3 | Detector catalogue page<br>No open High bugs |
| [KAN-138](https://pranav01.atlassian.net/browse/KAN-138) | Forensics documentation and bug fixes | T5 | 8 | MVP | 3 | RCA and grounding explained with examples<br>No open High bugs |
| [KAN-139](https://pranav01.atlassian.net/browse/KAN-139) | Playwright E2E for main flow and UI polish | T6 | 8 | MVP | 5 | E2E from §20 green in CI<br>Every screen has loading/empty/error states |
