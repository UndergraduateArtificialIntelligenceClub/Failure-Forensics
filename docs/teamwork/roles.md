# Roles

Roles define primary ownership, not silos. Every PR is reviewed by someone from another role.

| Role | Owner | Name | Primary ownership | Secondary | Planned pts |
|---|---|---|---|---|---|
| Tech Lead & Architect | T1 | *TBD* | Scope, backlog, contracts, ADRs, integration, reviews, ceremonies, final demo | Reviews all data-model PRs; RCA ranking with T5 | 51 |
| SDK & Ingestion | T2 | *TBD* | Python SDK, span links, redaction, OTel mapping, OpenAI adapter, ingestion, trace assembly | Compare screen and analytics queries from Sprint 6 | 77 |
| Backend & Infrastructure | T3 | *TBD* | Database, migrations, product APIs, auth and API keys, Celery jobs, storage, security, CI/CD, staging | Retention, release candidate | 83 |
| AI Detection | T4 | *TBD* | Taxonomy, rule validators, statistics, DecisionGate (Jev + fallback), LLM judges | Agent benchmark faults with T7 | 58 |
| AI Forensics | T5 | *TBD* | RCA engine, propagation, candidate ranking, evidence, explanation, grounding gate | Diagnosis UI contracts with T6 | 67 |
| Frontend / UX | T6 | *TBD* | Next.js console: shell, traces, failures, review, evaluations, analytics, settings | Playwright E2E suite | 78 |
| Evaluation & Benchmarks | T7 | *TBD* | Benchmark apps A/B/C, fault injection, datasets, eval runner, regressions, accuracy report | ADR-007 evaluation methodology | 79 |

## Scrum roles

| Scrum role | Who |
|---|---|
| Product owner (sets priorities, runs the demo) | *TBD* |
| Scrum master (rotates each sprint) | *TBD* |
| Note taker (rotates) | *TBD* |

Filter Jira by `labels = owner-T1` (and so on) to see one person's work.