# Evidence and claim model

| | |
|---|---|
| Status | Draft for review |
| Owner | T5 AI Forensics (Sashreek) |
| Agree with | T3 (Mohib, builds the models in KAN-89), T6 (Kinjal, renders claims in KAN-94) |
| Review | T1 plus one more reviewer, as for any data-model change |
| Jira | [KAN-29](https://pranav01.atlassian.net/browse/KAN-29) |
| GitHub | [#9](https://github.com/UndergraduateArtificialIntelligenceClub/Failure-Forensics/issues/9) |

!!! note "AI use"
    Drafted with Claude (Claude Code) from the data model on this site and the FF Confluence pages. The owner reviews it and is responsible for it before review with T3, T6 and T1.

A diagnosis is a short explanation split into claims, and every claim must point at data we stored for that trace. `EvidenceRef` is a pointer to one piece of that data. `DiagnosisClaim` is one sentence of the explanation plus the evidence it cites. The evidence store ([KAN-68](https://pranav01.atlassian.net/browse/KAN-68)) creates the refs, the explainer ([KAN-93](https://pranav01.atlassian.net/browse/KAN-93)) may cite only their IDs, and the grounding gate ([KAN-105](https://pranav01.atlassian.net/browse/KAN-105)) checks each claim against them.

## Decisions

1. Evidence is its own table, not an attribute on spans. One claim often cites several spans, a signal and a document at once.
2. A ref locates its value with `span_id`, an optional `signal_id`, an optional `object_ref` and a JSON Pointer (`field_path`, RFC 6901). The draft's single `field_path / object_ref` field becomes two fields.
3. `content_hash` is the SHA-256 of the value the ref points at, not of the excerpt. The grounding gate re-reads the value and compares hashes.
4. Claims cite evidence through a join table. The API still returns `evidence_ids[]`.
5. Claims keep their order and the grounding gate's checks. Removed claims stay in the table, so the pre-gate explanation can be audited and the grounding rate measured.

## EvidenceRef

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | `ev_…` |
| `trace_id` | string | yes | Same trace as the diagnosis |
| `span_id` | string | no | Null only for trace-level metadata |
| `signal_id` | string | no | New. Set for `quality_signal` and `rule_result` |
| `source_type` | enum | yes | `span_input`, `span_output`, `document`, `tool_response`, `quality_signal`, `rule_result`, `metadata` |
| `object_ref` | string | no | New, split out of the draft. The span's `input_ref` or `output_ref` when the payload lives in object storage, otherwise null |
| `field_path` | string | yes | JSON Pointer into the base value below. `""` means the whole value |
| `excerpt_or_summary` | string | yes | Up to 500 characters, see privacy |
| `content_hash` | string | yes | `sha256:` plus 64 hex characters |
| `analysis_job_id` | string | no | New. The job that created the ref |
| `created_at` | timestamp | yes | New |

Refs are never updated. A new analysis of the same trace creates new refs.

### What each source type points at

`field_path` is resolved against a different base value for each source type.

| `source_type` | `span_id` | `signal_id` | Base value for `field_path` |
|---|---|---|---|
| `span_input` | required | null | The span's input payload |
| `span_output` | required | null | The span's output payload |
| `document` | required (the retrieval span) | null | The retrieval span's output. The pointer selects one document |
| `tool_response` | required (the tool span) | null | The tool span's output |
| `quality_signal` | the signal's span, or null | required | The signal's verdict fields: `detector_type`, `check_name`, `verdict`, `score`, `confidence`, `failure_family`, `failure_category` |
| `rule_result` | the signal's span, or null | required | The signal's `details` object (proposed field, see open questions) |
| `metadata` | required, or null for the trace | null | The span row without `input` and `output`, or the trace row |

`document` and `span_output` can point at the same bytes. Use `document` when the claim is about a retrieved document as a unit (its text, its rank), so the UI can show it as a document.

### Hashing

```text
content_hash = "sha256:" + sha256( canonical_json( resolve(base_value, field_path) ) )
canonical_json = UTF-8 JSON with sorted keys, no whitespace, non-ASCII kept as is
```

In Python that is `json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)`. To check a claim, the grounding gate resolves the pointer again, recomputes the hash and compares. A mismatch means the stored data changed or the ref is wrong, and every claim citing that ref fails its check.

The excerpt is not hashed. It can be cut short or redacted, and the gate checks claim text against the full value, not the excerpt.

### Excerpts and privacy

- The excerpt is built from the stored value, which has already passed SDK and server redaction (ADR-006). It never comes from raw input.
- Under the `metadata-only` capture policy there is no payload to quote. The excerpt is a summary built from metadata (for example "document kb_annual_refund at rank 2"), and payload-based refs may be missing. The evidence-sufficiency decision ([KAN-104](https://pranav01.atlassian.net/browse/KAN-104)) should then return `MORE_EVIDENCE`.
- Excerpts are traced content, so the explainer treats them as untrusted data, never as instructions (KAN-93).

## DiagnosisClaim

| Field | Type | Required | Notes |
|---|---|---|---|
| `id` | string | yes | |
| `diagnosis_id` | string | yes | |
| `position` | integer | yes | New. Order in the explanation, from 1 |
| `text` | string | yes | One sentence |
| `evidence_ids` | string[] | yes | Stored in a join table `diagnosis_claim_evidence (claim_id, evidence_id)`, returned as an array |
| `status` | enum | yes | `supported`, `inference`, `unsupported_removed` |
| `checks` | JSON | no | New. Written by the grounding gate, one entry per ID, number or quote found in the text |
| `created_at` | timestamp | yes | New |

| Status | Meaning | Shown in the console |
|---|---|---|
| `supported` | Every ID, number and quote in the text appears in the cited evidence | Yes |
| `inference` | Follows from the cited evidence but is not stated in it. Must cite at least one ref | Yes, labelled as an inference |
| `unsupported_removed` | The gate removed it. Kept for audit and for the grounding rate | No |

Rules:

- Every claim the gate keeps cites at least one ref, and every cited ref belongs to the diagnosis's trace.
- A claim that cites no evidence, or cites a ref from another trace, is `unsupported_removed`.
- Proposed grounding rate for ADR-007: (`supported` + `inference`) ÷ all claims the explainer wrote.

## Examples

All examples come from fixture `rag-01` (the reranker demo case) in `backend/tests/fixtures/rca/`. The hashes are real: they were computed from the fixture values with the rule above. The IDs `ev_12` to `ev_15` line up with the KAN-31 wireframe.

### One ref per source type

| ID | `source_type` | Span | `field_path` | Value it points at |
|---|---|---|---|---|
| `ev_12` | `document` | `rag.retriever` | `/documents/1` | The `kb_annual_refund` document at rank 2, with its text |
| `ev_13` | `quality_signal` | `rag.retriever` | `""` | `retrieval_relevance` pass, score 0.88 |
| `ev_14` | `rule_result` | `rag.reranker` | `""` | `{doc_id: kb_annual_refund, rank_before: 2, rank_after: 8, context_cutoff: 5}` |
| `ev_15` | `span_output` | `rag.context_builder` | `/context_doc_ids` | The five context documents, without `kb_annual_refund` |
| `ev_16` | `metadata` | `rag.context_builder` | `/attributes/top_k` | `5` |
| `ev_17` | `span_input` | `rag.reranker` | `/candidate_doc_ids/1` | `"kb_annual_refund"`, second in the reranker's input |
| `ev_18` | `span_output` | `rag.reranker` | `/documents/7` | `kb_annual_refund` at rank 8 |
| `ev_19` | `span_output` | `rag.generator` | `/answer` | "You can get a refund within 14 days of the charge." |
| `ev_t1` | `tool_response` | an agent tool span | `/result` | `15000` (illustrative: no agent fixture exists yet) |

??? example "Full JSON for the refs"
    ```json
    [
      {"id": "ev_12", "trace_id": "65fb8d6ec4541c0ae44a9eae42865575", "span_id": "97ad675bf01fef09", "signal_id": null,
       "source_type": "document", "object_ref": null, "field_path": "/documents/1",
       "excerpt_or_summary": "kb_annual_refund (retriever rank 2): Annual plans can be refunded in full within 30 days of purchase. After 30 days, annual plans are not refundable.",
       "content_hash": "sha256:c5cd40df94410d8125e5a2a9020ea46bae3301ed45696db007c46847a42994dc",
       "analysis_job_id": "job_rag01_01", "created_at": "2026-11-12T19:00:05.000Z"},
      {"id": "ev_13", "trace_id": "65fb8d6ec4541c0ae44a9eae42865575", "span_id": "97ad675bf01fef09", "signal_id": "sig_rag01_02",
       "source_type": "quality_signal", "object_ref": null, "field_path": "",
       "excerpt_or_summary": "retrieval_relevance: pass (score 0.88, confidence 0.9)",
       "content_hash": "sha256:ccc4eaa8469a164257c1c29369d25164cf778190873e66035f5039030a2d3374",
       "analysis_job_id": "job_rag01_01", "created_at": "2026-11-12T19:00:05.000Z"},
      {"id": "ev_14", "trace_id": "65fb8d6ec4541c0ae44a9eae42865575", "span_id": "aab57338e4a8f0d9", "signal_id": "sig_rag01_03",
       "source_type": "rule_result", "object_ref": null, "field_path": "",
       "excerpt_or_summary": "relevant_doc_rank_drop: kb_annual_refund moved from rank 2 to rank 8 (context cutoff 5)",
       "content_hash": "sha256:b6b9b1af73db163a1c31974484d8652533238f5ba1c1764af2d4b28a062e72f1",
       "analysis_job_id": "job_rag01_01", "created_at": "2026-11-12T19:00:05.000Z"},
      {"id": "ev_15", "trace_id": "65fb8d6ec4541c0ae44a9eae42865575", "span_id": "9ed071cab164eacc", "signal_id": null,
       "source_type": "span_output", "object_ref": null, "field_path": "/context_doc_ids",
       "excerpt_or_summary": "Context documents: kb_monthly_refund, kb_trial, kb_cancel_steps, kb_enterprise_terms, kb_payment_methods",
       "content_hash": "sha256:6efe50a2e5cfe857ccbb59a04e72e553f2b2b3e015806c6ee99e98504afcd4e2",
       "analysis_job_id": "job_rag01_01", "created_at": "2026-11-12T19:00:05.000Z"},
      {"id": "ev_16", "trace_id": "65fb8d6ec4541c0ae44a9eae42865575", "span_id": "9ed071cab164eacc", "signal_id": null,
       "source_type": "metadata", "object_ref": null, "field_path": "/attributes/top_k",
       "excerpt_or_summary": "context_builder top_k = 5",
       "content_hash": "sha256:ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d",
       "analysis_job_id": "job_rag01_01", "created_at": "2026-11-12T19:00:05.000Z"},
      {"id": "ev_17", "trace_id": "65fb8d6ec4541c0ae44a9eae42865575", "span_id": "aab57338e4a8f0d9", "signal_id": null,
       "source_type": "span_input", "object_ref": null, "field_path": "/candidate_doc_ids/1",
       "excerpt_or_summary": "Reranker input position 2: kb_annual_refund",
       "content_hash": "sha256:59ef4b38899267c60877d68600e22d2b3cee4b2fd94d70df01babf7a941a64ae",
       "analysis_job_id": "job_rag01_01", "created_at": "2026-11-12T19:00:05.000Z"},
      {"id": "ev_18", "trace_id": "65fb8d6ec4541c0ae44a9eae42865575", "span_id": "aab57338e4a8f0d9", "signal_id": null,
       "source_type": "span_output", "object_ref": null, "field_path": "/documents/7",
       "excerpt_or_summary": "Reranker output rank 8: kb_annual_refund (score 0.46)",
       "content_hash": "sha256:f01d63ff9702a40f213796047a5532bca74bba01b48b8f137fe71d442a1f13b6",
       "analysis_job_id": "job_rag01_01", "created_at": "2026-11-12T19:00:05.000Z"},
      {"id": "ev_19", "trace_id": "65fb8d6ec4541c0ae44a9eae42865575", "span_id": "2c5bcd303175341d", "signal_id": null,
       "source_type": "span_output", "object_ref": null, "field_path": "/answer",
       "excerpt_or_summary": "Generator answer: You can get a refund within 14 days of the charge.",
       "content_hash": "sha256:a1e545ac86daf1983915b49f5acf65a5c7939116aa6d26707d3b6260d5199dc3",
       "analysis_job_id": "job_rag01_01", "created_at": "2026-11-12T19:00:05.000Z"},
      {"id": "ev_t1", "trace_id": "<agent trace>", "span_id": "<agent.tool_executor span>", "signal_id": null,
       "source_type": "tool_response", "object_ref": null, "field_path": "/result",
       "excerpt_or_summary": "calculator(1250 * 12) returned 15000",
       "content_hash": "sha256:d4c999ae43633bd2036188d2bca68e1be8202b2cc1f3a1c42a728eaff7d2483d",
       "analysis_job_id": "<job>", "created_at": "<time>"}
    ]
    ```

### Claims for the demo diagnosis

| # | Claim | Cites | Status | Why |
|---|---|---|---|---|
| 1 | The correct document, kb_annual_refund, was retrieved at rank 2. | ev_12, ev_13 | `supported` | ID and rank are in ev_12 |
| 2 | The reranker moved it to rank 8. | ev_14, ev_18 | `supported` | Rank 8 is in ev_14 and ev_18 |
| 3 | The top-5 context cutoff removed it from the context. | ev_15, ev_16 | `supported` | `top_k = 5` in ev_16, document missing from ev_15 |
| 4 | Without that document, the generator used the 14-day monthly-plan window instead. | ev_15, ev_19 | `inference` | "14 days" is in ev_19, but the cause is reasoned, not stated |
| 5 | The reranker model was updated last week. | none | `unsupported_removed` | Nothing in the trace says this |

The grounding gate's `checks` for claim 2:

```json
[
  {"kind": "number", "value": "8", "evidence_id": "ev_14", "field": "rank_after", "passed": true},
  {"kind": "number", "value": "8", "evidence_id": "ev_18", "field": "rank", "passed": true}
]
```

## Alternatives considered

| Option | Why not |
|---|---|
| Evidence as span attributes (`ff.evidence_refs`, ADR-003 gap 4) | A claim cites several spans and signals, and each ref needs its own hash and excerpt. A table keeps that queryable. |
| `evidence_ids` as a Postgres array on the claim | No foreign keys, and "which claims cite this ref" needs a scan. The join table costs one extra table. |
| Hash the excerpt | The excerpt can be truncated or redacted, so its hash proves nothing about the stored value. |
| One locator string such as `span:aab5…/output#/documents/7` | Harder to validate and query than separate fields. |

## Changes to the draft data model

Compared with [Data Model](data-model.md):

- `EvidenceRef`: `field_path / object_ref` split into `object_ref` (nullable) and `field_path` (JSON Pointer). Added `signal_id`, `analysis_job_id`, `created_at`. `content_hash` gains a `sha256:` prefix.
- `DiagnosisClaim`: added `position`, `checks`, `created_at`. `evidence_ids[]` backed by a join table.
- `QualitySignal`: proposed `details` object, needed by `rule_result` refs.

The data-model page will be updated once T3 and T1 agree.

## Open questions

1. **`rule_result` versus `quality_signal`.** These only differ if `QualitySignal` gets a `details` field (also open question 6 on the RCA page). Without it, `rule_result` should be dropped from the enum. For T4 and T1.
2. **Grounding rate.** ADR-007 says "% of diagnosis claims linked to stored evidence after the gate". Measured after the gate it is always 100%, so the proposal above counts claims that survive out of all claims written. For T7.
3. **Who creates refs.** Proposed: the evidence store creates refs for the root cause, every span on the propagation path and their signals before the explainer runs, and the explainer may cite only those. For T1.
4. **Excerpt length.** 500 characters is a guess. For T6, based on what the investigation page can show.
5. **Join table or array.** The final call is T3's in KAN-89.
