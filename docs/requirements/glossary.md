# Glossary

| Term | Meaning |
|---|---|
| **Trace** | One complete end-to-end execution of an AI request. |
| **Span** | One operation within a trace (an LLM call, a retrieval, a tool call, and so on). |
| **Span link** | A data-flow edge: span B consumed the output of span A (`relation: consumes_output_of`). |
| **Component key** | Stable name of a pipeline step, such as `rag.reranker`, that stays the same across runs. Used to match expected root causes in regression runs. |
| **Quality signal** | The result of one check on a span or trace: a rule, a statistic, a DecisionGate decision, an LLM judge or a user flag. |
| **DecisionGate** | Interface for fast bounded classifications with a confidence score (PASS/FAIL/REVIEW, failure family, evidence sufficiency). |
| **Jev** | The bounded-decision model named in the original blueprint, used as one DecisionGate backend. An LLM classifier is the fallback. *Open question: what Jev is and how we access it (ADR-004).* |
| **Failure family / category** | Two-level taxonomy, such as `RETRIEVAL / RERANKING_FAILURE`. Defined once in `taxonomy.py`. |
| **Root cause** | The earliest causal operation that introduced the significant failure. |
| **Propagation** | Downstream reuse or transformation of an earlier incorrect state. |
| **Span role** | A span's part in a diagnosis: `healthy`, `root_cause`, `propagated`, `degraded`, `failed_output`, `unknown`. |
| **Evidence** | Stored trace data supporting a diagnostic claim (`EvidenceRef`). |
| **Grounding gate** | Step that checks every claim in a diagnosis against stored evidence and removes unsupported claims. |
| **Eval case** | A reusable input and expectation pair used to test future pipeline versions. |
| **Regression** | A previously passing case that fails after a change. |
| **Fault injection** | Deliberately creating a controlled failure with a known root cause in a benchmark app. |
| **MVP / Target / Stretch** | Scope tiers. MVP ships by M2 (29 Jan), Target by M3 (12 Feb), Stretch only if time allows. |
| **ADR** | Architecture Decision Record, stored in Confluence and `docs/adr/`. |
| **UAIS** | Used in the blueprint headers. *Open question: confirm what it stands for (possibly the club's name).* |
