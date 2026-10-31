# Testing

## Strategy

| Level | Coverage | Tools |
|---|---|---|
| Unit | Pydantic validators, trace assembly, link building, rules, ranking, grounding, taxonomy | pytest |
| Integration | FastAPI + PostgreSQL + Redis + MinIO, SDK → ingestion, worker jobs, provider adapters with stubs | pytest, Testcontainers |
| Contract | SDK and backend schemas match, OpenAPI responses, generated TypeScript types in sync | pytest, CI diff check |
| Frontend component | Trace nodes, drawers, tables, filters, diagnosis cards | Vitest, React Testing Library |
| End-to-end | Instrument app → ingest → view → flag → analyze → confirm → eval case → rerun | Playwright |
| AI evaluation | Golden cases and injected faults with known root cause (dev and held-out) | Eval harness (KAN-96) |
| Security | Secret redaction, cross-project access, oversized payloads, prompt injection in traced text | pytest (KAN-135) |
| Load (stretch) | Burst ingestion, 500-span traces, concurrent analyses | Locust or k6 (KAN-125) |

## PR gates

Ruff and mypy · backend unit tests · frontend lint, type-check and tests · Alembic migration check on schema changes · Docker build smoke test on `main`.

## Accuracy evaluation

- Benchmarks are split into **dev** and **held-out** by fault type and seed.
- The RCA engine is tuned on dev only.
- The held-out set is run **once**, in Sprint 8 (KAN-127), and reported in the evaluation report (KAN-140).

| Benchmark | Pipeline | Built | Example faults |
|---|---|---|---|
| A: Document | Extraction → Classification → Summarization | Sprint 2 | Hallucinated entity, omitted amount, schema violation |
| B: RAG | Rewrite → Retrieval → Rerank → Context → LLM | Sprints 3–4 | Corrupted ranking, top-k cutoff removes truth, broken citations |
| C: Agent | Planner → Tool selection → Tool call → Reasoning | Sprints 5–6 | Wrong tool, malformed arguments, loop, premature stop |

## Final demo script

1. Open the RAG benchmark and ask a factual question.
2. Inject a reranking failure: the correct source is retrieved but pushed below the context cutoff.
3. Show the wrong final answer.
4. Open Failure Forensics and inspect the trace.
5. Show the reranker as root cause and context and generation spans as propagated or degraded.
6. Show the evidence proving the correct document existed before reranking.
7. Show the rule, DecisionGate and judge signals and the grounded diagnosis.
8. Confirm the diagnosis as a reviewer; an eval case is created.
9. Apply a reranker configuration fix and run the regression suite.
10. The case changes from FAIL to PASS.

Each step has a fallback screen recording (KAN-121).

## Test reports

Link CI runs and coverage reports here each sprint.
