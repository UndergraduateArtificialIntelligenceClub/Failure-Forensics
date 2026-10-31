# Research

## Related tools

| Tool | What it does well | Gap Failure Forensics fills |
|---|---|---|
| LangSmith, Langfuse, Arize Phoenix | Trace LLM calls, show spans and prompts, run evaluators | Show *where* a failure started and *how* it spread, with grounded evidence |
| OpenTelemetry | Vendor-neutral tracing standard, span links | No AI-specific failure analysis |
| Datadog, Grafana | Infrastructure metrics and logs | Not designed for semantic AI failures |
| RAG evaluation frameworks (e.g. RAGAS) | Score retrieval and answer quality | Scores the whole pipeline, does not localize the cause |

## Technical spikes (Sprint 1)

| Spike | Owner | Jira | Output |
|---|---|---|---|
| SDK API shape including `inputs_from` links | T2 | KAN-19 | Spike branch and review |
| Span model to OpenTelemetry attribute mapping | T2 | KAN-20 | Mapping table |
| What Jev is and how it is accessed | T4 | KAN-27 | Recommendation for ADR-004 |
| Root-cause algorithm design and fixtures | T5 | KAN-28 | Design doc and 6+ fixture traces |
| Benchmark workloads and evaluation methodology | T7 | KAN-32, KAN-33 | Pipeline definitions, metric definitions |

## Architecture Decision Records

| ADR | Decision | Due |
|---|---|---|
| ADR-001 | Modular monolith with async workers | M0, 13 Nov |
| ADR-002 | PostgreSQL for metadata, object store for payloads | M0 |
| ADR-003 | OpenTelemetry compatibility and span links | M0 |
| ADR-004 | DecisionGate boundary and Jev backend | M0 |
| ADR-005 | Celery workers on Redis | M0 |
| ADR-006 | Capture modes, retention and privacy | M0 |
| ADR-007 | Evaluation methodology (dev / held-out split, metrics) | Sprint 4, 23 Dec |

Record findings from each spike here and link the Confluence page.
