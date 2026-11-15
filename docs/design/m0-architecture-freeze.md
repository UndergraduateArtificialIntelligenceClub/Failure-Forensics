# M0 Architecture Freeze

**Effective date:** 13 November 2026  
**Recorded:** 14 November 2026  
**Jira:** [KAN-18](https://pranav01.atlassian.net/browse/KAN-18)

The team freezes the following contract, success targets, and MVP scope for M0. Changes after this point require a reviewed ADR or Blueprint erratum and must include migration and test updates.

## Trace contract

The canonical executable contract is implemented by the Pydantic `Trace`, `Span`, and `SpanLink` models in `sdk/python/failure_forensics/models.py`.

- Trace IDs are 128-bit lowercase hexadecimal strings; span IDs are 64-bit lowercase hexadecimal strings.
- Every span belongs to exactly one trace and may reference one parent span in that trace.
- `component_key` is the stable identifier used across executions and evaluation cases.
- A span link is directed from producer to consumer. The default relation is `consumes_output_of`.
- Trace status is `ok`, `error`, or `incomplete`.
- Span status is `ok`, `error`, `timeout`, or `cancelled`.
- Span types are `llm`, `retrieval`, `reranker`, `tool`, `agent`, `transform`, `guardrail`, and `custom`.
- Timestamps, latency, token counts, cost, payload references, model metadata, errors, and extensible attributes are part of the contract.
- Unknown fields are rejected so contract changes are deliberate and reviewed.

The contract follows ADR-003 and the data model. OpenTelemetry compatibility is maintained through OTel-shaped IDs, timestamps, status, attributes, `gen_ai.*` mappings, and explicit span links. Failure Forensics-specific metadata uses the `ff.*` namespace when exported to OTel.

## Confirmed success targets

The §2.5 targets are confirmed without changes:

| Metric | Frozen target |
|---|---:|
| Root-cause Top-1 accuracy | ≥ 60% |
| Root-cause Top-3 accuracy | ≥ 85% |
| Classification macro-F1 | ≥ 0.70 |
| Evidence grounding rate | ≥ 95% |
| False positive rate on healthy traces | ≤ 10% |
| Diagnosis latency | p95 ≤ 60 seconds |
| Human override rate | Reported; no pass/fail threshold for V1 |

The evaluation harness measures these targets on the held-out benchmark set in Sprint 8. Development data is used for tuning; held-out data is not used for tuning.

## Frozen MVP scope

MVP remains due at M2 on 29 January 2027 and includes:

- manual SDK traces, spans, and data-flow links;
- document and RAG benchmarks;
- deterministic validators and one semantic LLM judge;
- one evidence-grounded root cause;
- the trace explorer and failures page;
- human flagging, feedback, and evaluation-case creation; and
- Docker Compose deployment.

Items in the Target and Stretch tiers remain outside MVP unless an approved scope change moves them. The existing non-goals remain unchanged.

## Verification

- Pydantic contract unit tests validate identifiers, graph references, timing, status/type enums, link direction, and rejection of unreviewed fields.
- The SDK validates every completed trace against the frozen contract before export.
- Documentation and CI checks must pass before this freeze record is merged.
