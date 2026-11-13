# Wireframes

Low-fidelity wireframes for the developer console, produced in Sprint 1 (KAN-31, owner T6) and reviewed with T1 and T5. Every image is a 1280 × 800 frame. All names, numbers and traces shown are sample data.

## Navigation

`Overview · Live traces · Traces · Failures · Compare · Evaluations · Experiments · Datasets · Analytics · Settings`

Live traces is a stretch goal. Trace detail has no menu item: it opens when a trace row is clicked.

Colour means role: green = healthy, red = root cause or failed output, amber = propagated or degraded. Role names are always shown as text as well.

## Traces

![Traces list with search, filters and a table of traces](../assets/wireframes/03a_traces_list.png){ loading=lazy }

*Traces list: search, filters (status, date, model, pipeline version, flagged only) and a sortable table. Clicking a row opens Trace detail.*
![Traces list loading state with skeleton rows](../assets/wireframes/03b_traces_loading.png){ loading=lazy }

*Loading state.*
![Traces list empty state asking the user to send a first trace](../assets/wireframes/03c_traces_empty.png){ loading=lazy }

*Empty state: no traces yet.*
![Traces list with no results for the current filters](../assets/wireframes/03d_traces_no_match.png){ loading=lazy }

*Empty state: no traces match the filters.*
![Traces list error state with a retry button](../assets/wireframes/03e_traces_error.png){ loading=lazy }

*Error state with a request ID and a retry button.*

## Trace detail

![Trace detail chain view with span details panel](../assets/wireframes/04a_trace_detail_chain.png){ loading=lazy }

*Chain view with the span details panel (latency, tokens, cost, version, input, output, quality signals).*
![Trace detail dependency graph view](../assets/wireframes/04b_trace_detail_graph.png){ loading=lazy }

*Graph view: solid lines are parent/child, dashed lines are data-flow links.*
![Trace detail timeline view](../assets/wireframes/04c_trace_detail_timeline.png){ loading=lazy }

*Timeline view.*
![Trace detail loading state](../assets/wireframes/04d_trace_detail_loading.png){ loading=lazy }

*Loading state.*
![Trace detail not found state](../assets/wireframes/04e_trace_detail_not_found.png){ loading=lazy }

*Not-found state.*
![Trace detail error state](../assets/wireframes/04f_trace_detail_error.png){ loading=lazy }

*Error state.*

??? note "Original text sketch of the trace explorer"

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

## Failures investigation

![Failures investigation page with root cause, propagation, ranked causes and evidence timeline](../assets/wireframes/05a_failures_diagnosis.png){ loading=lazy }

*Diagnosis ready: root cause, confidence, propagation path, ranked causes and review controls. The evidence timeline is a stretch item (KAN-107).*
![Failures page while the analysis job is running](../assets/wireframes/05b_failures_running.png){ loading=lazy }

*Analysis running, with progress steps.*
![Failures page with no diagnosis yet](../assets/wireframes/05c_failures_empty.png){ loading=lazy }

*Empty state: no analysis has been run for this trace.*
![Failures page showing an inconclusive diagnosis](../assets/wireframes/05d_failures_inconclusive.png){ loading=lazy }

*Inconclusive state: low confidence, closest candidates shown.*
![Failures page error state when the analysis fails](../assets/wireframes/05e_failures_error.png){ loading=lazy }

*Error state: analysis failed.*
![Correct diagnosis pop-up over the failures page](../assets/wireframes/05f_failures_correct_modal.png){ loading=lazy }

*Review pop-up: correct the diagnosis (an evaluation case is created).*

??? note "Original text sketch of the failures investigation"

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

## Other console screens

These are outside the KAN-31 scope and are drawn so the whole console is covered. Details will change as each screen is built.

![Overview dashboard](../assets/wireframes/01a_overview.png){ loading=lazy }

*Overview: reliability KPIs, failures over time, top failure categories, recent critical traces.*
![Live traces stream](../assets/wireframes/02a_live_traces.png){ loading=lazy }

*Live traces (stretch goal): new traces appear as they arrive.*
![Live traces waiting for traces](../assets/wireframes/02b_live_traces_waiting.png){ loading=lazy }

*Live traces: waiting state.*
![Compare screen with a healthy and a failed trace side by side](../assets/wireframes/06a_compare.png){ loading=lazy }

*Compare (Target, KAN-110): healthy and failed trace side by side with the first divergence.*
![Evaluations screen with run summary, known issue resolution and cases](../assets/wireframes/07a_evaluations.png){ loading=lazy }

*Evaluations (Target, KAN-118): latest run, release gate, known issue resolution and cases.*
![Experiments screen comparing two versions](../assets/wireframes/08a_experiments.png){ loading=lazy }

*Experiments (Stretch, KAN-128).*
![Datasets screen with a case list](../assets/wireframes/09a_datasets.png){ loading=lazy }

*Datasets: golden and failure cases.*
![Analytics screen with six charts](../assets/wireframes/10a_analytics.png){ loading=lazy }

*Analytics (Target, KAN-129): failures by step and model, cost vs quality, latency, override rate, MTTD / MTTR.*
![Settings screen on the API keys tab](../assets/wireframes/11a_settings_api_keys.png){ loading=lazy }

*Settings (MVP, KAN-69): API keys tab.*
![Settings screen on the Integrations tab](../assets/wireframes/11b_settings_integrations.png){ loading=lazy }

*Settings: Integrations tab.*

### Settings (MVP)

Projects, API keys (create, revoke, shown once), provider keys, capture policy (metadata-only, sampled, full), retention days.
