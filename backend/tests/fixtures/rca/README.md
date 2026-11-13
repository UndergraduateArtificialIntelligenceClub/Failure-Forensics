# RCA fixture traces

Hand-built traces with a known root cause, for testing the root-cause engine before the detectors and benchmark apps exist. They come from [KAN-28](https://pranav01.atlassian.net/browse/KAN-28). [KAN-45](https://pranav01.atlassian.net/browse/KAN-45) turns them into pytest cases. The algorithm they test is described in `docs/design/rca-algorithm.md`.

## Files

| Fixture | Workload | Root cause | Category | What it tests |
|---|---|---|---|---|
| `rag-01-reranker-demotes-relevant-doc` | RAG | `rag.reranker` | RETRIEVAL / RERANKING_FAILURE | The demo case. Root cause in the middle of the chain. |
| `rag-02-relevant-doc-missing` | RAG | `rag.retriever` | RETRIEVAL / RETRIEVAL_MISS | Bad state carried through four later steps. A rule that returns `unknown` is ignored. |
| `rag-03-topk-cutoff-drops-relevant-doc` | RAG | `rag.context_builder` | CONFIGURATION / PARAMETER_REGRESSION | Category comes from the strongest signal that has one. |
| `rag-04-retriever-timeout` | RAG | `rag.retriever` | PIPELINE / TIMEOUT | Operational error. A span with no signals on the path gets `unknown`. RCA v0 must pass this one. |
| `rag-05-healthy` | RAG | none | none | No failure. RCA must not invent a root cause. |
| `rag-06-reranker-demotes-no-links` | RAG | `rag.reranker` | RETRIEVAL / RERANKING_FAILURE | Same run as rag-01 with no span links. Fallback edges give the same answer at lower confidence. |
| `doc-01-hallucinated-entity` | Document | `doc.extraction` | MODEL / HALLUCINATION | Fan-out. A downstream step that stays correct is `healthy`, not `propagated`. |
| `doc-02-summary-omits-amount` | Document | `doc.summarization` | MODEL / INSTRUCTION_FAILURE | Root cause at the last step. Healthy upstream steps are not blamed. |
| `doc-03-schema-violation` | Document | `doc.extraction` | PIPELINE / SCHEMA_FAILURE | The exception surfaces one step later than the cause. RCA v0 gets this wrong by design. |

## Format

One JSON object per file, `fixture_format: 1`.

| Key | Contents |
|---|---|
| `fixture_id`, `workload`, `description` | What the fixture is and why it exists. |
| `fault` | The injected fault (`fault_type`, `target_component_key`, `injection_parameters`), or `null` for the healthy trace. A subset of `InjectedFault`. |
| `trace` | One `Trace` row, with fields from `docs/design/data-model.md`. |
| `spans` | `Span` rows. `input` and `output` are inline JSON instead of `input_ref` / `output_ref`, so the files stay readable. A loader writes them to object storage or inlines them. |
| `links` | `SpanLink` rows (`from_span_id` is the producer, `to_span_id` is the consumer). |
| `signals` | `QualitySignal` rows. Hand-written stand-ins for what the detectors (KAN-42 to KAN-80) will produce, so RCA can be tested on its own. `details` is a proposed new field, see the design doc. |
| `flags` | `Flag` rows. Each user flag also appears in `signals` as a `user_flag` signal on the root span. |
| `expected` | The answer, keyed by `component_key` so it doesn't depend on span IDs. |

`expected` contains:

- `status`: `diagnosed`, `inconclusive` or `no_failure`.
- `min_rca_version`: `v0` if RCA v0 (KAN-59, earliest operational error) should already pass, otherwise `v1` (KAN-81).
- `root_cause_component`, `root_cause_span_type`, `failure_family`, `failure_category`.
- `propagation_path`: component keys from the root cause to the failed output, in data-flow order.
- `span_roles`: one role per component key.
- `link_source`: `links` if the path uses only recorded span links, `fallback` if any edge was inferred.
- `confidence_range`: `[low, high]` bounds rather than an exact number, because the confidence formula will be tuned.

IDs, timestamps and costs are made up but consistent. Trace IDs are 32 hex characters and span IDs are 16, matching OpenTelemetry. All data is synthetic.

## Suggested assertions for KAN-45

- For RCA v0, assert only `status` and `root_cause_component`, and mark fixtures with `min_rca_version: v1` as `xfail`.
- For RCA v1, assert `status`, the root cause fields, the category and `propagation_path` exactly. Assert `link_source` and that confidence falls in `confidence_range`.
- `span_roles` for `propagated` versus `degraded` depends on the provisional threshold ε, so expect to update those two values when the thresholds are tuned (KAN-117).
