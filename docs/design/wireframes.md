# Wireframes

Low-fidelity wireframes are produced in Sprint 1 (KAN-31, owner T6) and reviewed with T1 and T5. Add exported images to `docs/assets/wireframes/` and embed them here.

## Navigation

`Overview · Traces · Compare · Failures · Evaluations · Experiments · Datasets · Analytics · Settings`

## Trace explorer (MVP)

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ Traces › 7f3a…  rag-v3   status: ok   health: failed   1.8 s  $0.0042   │
├───────────────────────────────────────────┬──────────────────────────────┤
│  [question]                                │ Span: reranker               │
│      │                                     │ component: rag.reranker      │
│  [query rewrite] ──▶ [retrieval] ●green    │ role: ROOT CAUSE  (0.82)     │
│                          │                 │ input: 20 docs               │
│                     [reranker] ●red        │ output: doc_17 moved 2 → 8   │
│                          │                 │ signals: rule ✔, judge ✘     │
│                  [context build] ●amber    │ [Input] [Output] [Signals]   │
│                          │                 │                              │
│                     [generator] ●amber     │ [ Flag ]  [ Analyze ]        │
│                          │                 │                              │
│                   [answer] ●red            │                              │
├───────────────────────────────────────────┴──────────────────────────────┤
│ Timeline  ▇▇ rewrite ▇▇▇▇ retrieval ▇▇ rerank ▇ context ▇▇▇▇▇▇ generate   │
└──────────────────────────────────────────────────────────────────────────┘
```

## Failures investigation (MVP)

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ Diagnosis  RETRIEVAL / RERANKING_FAILURE   confidence 0.82   grounded ✔ │
├──────────────────────────────────────────────────────────────────────────┤
│ Root cause: rag.reranker                                                 │
│ Path: reranker → context build → generator → answer                      │
│ Claims                                                     Evidence      │
│  1. The correct document was retrieved at rank 2.          ev_12, ev_13  │
│  2. The reranker moved it to rank 8.                       ev_14         │
│  3. The top-5 cutoff removed it from the context.          ev_15         │
│ Review:  ( Confirm )  ( Correct… )  ( Unsure )                           │
└──────────────────────────────────────────────────────────────────────────┘
```

## Settings (MVP)

Projects, API keys (create, revoke, shown once), provider keys, capture policy (metadata-only, sampled, full), retention days.
