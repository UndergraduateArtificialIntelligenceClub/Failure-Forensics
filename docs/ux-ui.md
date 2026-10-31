# UX and UI Design

## Principles

- **Show the cause, not just the log.** The first thing on a failed trace is the root-cause span and the path the error took.
- **Every claim is clickable.** Each sentence in a diagnosis links to the evidence that supports it.
- **Colour means role.** Green = healthy, red = root cause or failed output, amber = propagated or degraded, grey = unknown. Colour is never the only cue: role names are always shown as text.
- **Every screen has loading, empty and error states** (part of the Definition of Done).
- **Fast first trace.** A new user installs the SDK and sees a first trace in under 10 minutes.

## Screens

| Screen | Purpose | Tier | Jira |
|---|---|---|---|
| Console shell and navigation | Layout, routing, generated API client | MVP | KAN-46 |
| Traces list | Search and filter by status, health, version, date | MVP | KAN-47 |
| Trace DAG view | React Flow graph coloured by status and role | MVP | KAN-60 |
| Timeline and span drawer | Gantt timeline, input/output, tokens, cost | MVP | KAN-61, KAN-70 |
| Settings | Projects, API keys, capture policy | MVP | KAN-69 |
| Flag and analysis progress | Flag a trace, watch the job | MVP | KAN-82 |
| Failures list | Diagnoses with category, confidence, status | MVP | KAN-83 |
| Investigation page | Root cause, roles, claims, evidence | MVP | KAN-94 |
| Review controls | Confirm, correct, unsure | MVP | KAN-106 |
| Evaluations | Datasets, cases, regression runs | Target | KAN-118 |
| Compare | Healthy vs failed trace, first divergence | Target | KAN-110 |
| Analytics dashboard | KPIs, failures over time, cost and latency | Target | KAN-129 |
| Evidence timeline | Evidence ordered by time | Stretch | KAN-107 |
| Experiments | Compare versions | Stretch | KAN-128 |

## Hero interaction

The trace explorer colours spans by diagnostic role and shows the diagnosis, confidence and propagation path beside the graph. This is the core of the final demo (see [Testing](testing.md#final-demo-script)).

## Accessibility

- Contrast ratio of at least 4.5:1 for text.
- Keyboard navigation for the graph (tab through spans, Enter opens the drawer).
- Role labels as text next to colours.
