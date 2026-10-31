# Executive Summary

Failure Forensics is a developer platform for observing, diagnosing, evaluating and preventing failures in AI applications built from many steps: LLM calls, retrieval, reranking, tools and agents. These systems often return an answer that is technically successful but semantically wrong.

The platform captures a complete execution trace, evaluates each step, finds the **earliest significant failure**, reconstructs how it **propagated**, produces an **evidence-backed diagnosis**, lets a human confirm or correct it, and turns confirmed failures into **regression cases**.

!!! quote "Core product question"
    When an AI application gives a bad final answer, where did the failure first originate, how did it propagate, and what evidence proves it?

## Project outcomes

- A reusable Python instrumentation SDK for AI applications.
- An OpenTelemetry-compatible trace and span model, including **data-flow links** between spans.
- A backend that ingests and stores AI execution traces.
- A hybrid detection layer: deterministic validators, statistics, a DecisionGate classifier and LLM judges.
- A forensics engine that localizes root causes and tracks propagation.
- Evidence-grounded diagnoses that reject unsupported claims.
- A human-in-the-loop workflow that creates evaluation cases from confirmed failures.
- A regression runner for comparing prompts, models, retrievers and pipeline versions.
- A Next.js developer console.
- A benchmark suite with controlled fault injection across document, RAG and agent workloads.

## Scope

=== "MVP (by 29 Jan 2027, M2)"
    - Manual SDK spans and links
    - Document and RAG benchmarks
    - Rule validators and one semantic LLM judge
    - Single root cause with evidence and grounding
    - Trace explorer and failures page
    - Human flag, feedback and eval case
    - Docker Compose deployment

=== "Target (by 12 Feb 2027, M3 feature freeze)"
    - OpenAI, retrieval and tool auto-instrumentation
    - Simple agent benchmark
    - DecisionGate (Jev backend if available) and LLM fallback
    - Ranked candidate causes and propagation path
    - Compare screen, evaluations UI, analytics dashboard
    - Regression runner
    - Shared staging deployment

=== "Stretch (only if time allows)"
    - Evidence timeline view, extra LLM judges, offline tool-call assessment
    - Analytics overview API, JSON/CSV export, live (SSE) job progress
    - Load-test suite, experiments engine and screen
    - Anthropic, LangChain and LlamaIndex adapters

## Non-goals for V1

- Replacing enterprise observability platforms such as Datadog or Grafana.
- A general-purpose APM for arbitrary microservices.
- Training a foundation model.
- Supporting every LLM provider or agent framework.
- Autonomous remediation, including blocking or rewriting tool calls in the user's running app.
- Multi-region SaaS tenancy.

## Success metrics

Targets are proposals. The team confirms them in Sprint 1 and measures them on the held-out benchmark set in Sprint 8.

| Metric | Definition | Target |
|---|---|---|
| Root-cause Top-1 accuracy | % of injected failures whose true component is ranked first | ≥ 60% |
| Root-cause Top-3 accuracy | % where the true cause is in the top three | ≥ 85% |
| Classification macro-F1 | Mean over categories of the harmonic mean of precision and recall | ≥ 0.70 |
| Evidence grounding rate | % of diagnosis claims linked to stored evidence after the gate | ≥ 95% |
| False positive rate | % of healthy traces labelled failed | ≤ 10% |
| Diagnosis latency | Job start to diagnosis stored | p95 ≤ 60 s |
| Human override rate | % of reviewed diagnoses whose root cause was corrected | Reported |

## Key milestones

| Milestone | Date | Meaning |
|---|---|---|
| M0 Architecture freeze | 13 Nov 2026 | ADR-001 to 006 approved, trace/span contract frozen |
| M1 Vertical slice | 11 Dec 2026 | Benchmark → SDK → ingestion → storage → trace UI works |
| M2 MVP | 29 Jan 2027 | Flag → analyze → grounded diagnosis on document and RAG |
| M3 Feature freeze | 12 Feb 2027 | Only bug fixes, tests, docs after this |
| M4 Code complete | 26 Feb 2027 | Release candidate on staging, evaluation report |
| Final demo | Early March 2027 | Live demo (week 1 or 2 of March) |
