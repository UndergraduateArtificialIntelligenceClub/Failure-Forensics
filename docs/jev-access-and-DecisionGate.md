# KAN-27: Jev Access Investigation and DecisionGate Recommendation

This investigation supplies the T4 input to [ADR-004](https://pranav01.atlassian.net/wiki/spaces/FF/pages/1998849/ADR-004+DecisionGate+boundary+and+Jev+backend). Vendor-published performance claims are recorded as claims, not as measurements by the Failure Forensics team.

## 1. Jev investigation

### What Jev is

[TypeSafe describes Jev](https://docs.typesafe.ai/introduction) as its first System One model. Instead of generating prose, it evaluates typed questions against a shared state and returns structured answers, probability distributions and, for some question types, confidence values. The public primitives are:

- `choice`: choose one option and return probabilities plus confidence;
- `score`: select an ordered level and return probabilities plus confidence;
- `noul`: return the probability that a yes/no statement is true; and
- `box`: return image bounding-box coordinates plus confidence.

This is a different contract from asking a general-purpose LLM to produce JSON. Jev's options and output types are part of the request schema.

### API and access

The public [System One API](https://docs.typesafe.ai/api/system-one) accepts one `state` and one or more typed questions in a request. TypeSafe also publishes [Python](https://docs.typesafe.ai/sdk/python) and [JavaScript](https://docs.typesafe.ai/sdk/javascript) clients. The current public HTTP operation is `POST /v1/systemone`; requests require a TypeSafe API key and return one typed answer per question together with usage and model metadata.

Failure Forensics does **not** currently have an approved TypeSafe account, shared API key or budget. TypeSafe describes Jev as early access and says it is [bringing developers off the waitlist](https://typesafe.ai/blog/introducing-system-one-models-and-jev). Therefore, this project cannot validate authentication, response compatibility, service availability or account-specific limits yet. No credential or third-party gateway is required for the MVP.

### Cost

TypeSafe's published price is [$0.042 per million input tokens](https://help.typesafe.ai/articles/5187202169-how-much-does-jev-cost), with output tokens free. The same page states that there is no free trial and that standard accounts begin with published token and request-rate limits. These are vendor terms as of 14 November 2026 and may change.

Local open-weight models have no per-token vendor fee, but they still have compute, memory, deployment and maintenance costs. KAN-126 must report both hosted usage cost and local infrastructure cost on the same benchmark workload.

### Latency

TypeSafe advertises approximately [100 ms response speeds](https://typesafe.ai/blog/introducing-system-one-models-and-jev) and notes that its published measurements were generally taken from West Coast laptops while the service was hosted there. This is a vendor claim, not an SLA or a Failure Forensics measurement.

Actual end-to-end latency for our payload sizes, deployment region, concurrent load and network path is **unverified** because the team has no credentials. If access is approved, KAN-126 must measure p50 and p95 latency, timeouts and rate-limit behavior rather than reusing the vendor number.

### Impact

Jev cannot block the architecture freeze or MVP. It remains an optional adapter under KAN-103, contingent on access, team approval, privacy review and project-specific evaluation.

## 2. Recommendation for ADR-004

Adopt the vendor-neutral `DecisionGate.decide(decision_type, payload)` boundary already selected in ADR-004:

1. Run deterministic validators first when a rule can produce a clear result.
2. Use a model-backed gate only when classification or judgment is necessary.
3. Normalize every backend to the project contract: `verdict`, nullable canonical `failure_family`, nullable canonical `failure_category`, `confidence`, `review_required`, `backend` and `model_version`.
4. Route invalid output, backend errors, unsupported labels and low-confidence results to `REVIEW`.
5. Persist backend/version metadata for audit, but never persist unredacted inputs in decision logs.

### Open-source candidates

**Evaluate Laya Typed-Decisions first.** Its [model card](https://huggingface.co/convaiinnovations/laya-typed-decisions) lists 421M parameters, a 1,024-token context and an Apache 2.0 license. It is specialized for four synthetic workflows, including agent-trace observability. The same card warns that it may perform poorly outside those workflows and that its confidence is not yet calibrated. We must test taxonomy mapping, context fit, calibration, memory use and latency on our own dev split before adoption.

**Evaluate Kev second.** The [Kev repository](https://github.com/jaredpalmer/kev) publishes Apache 2.0 Jev-like models and a TypeSafe-compatible API. The 0.8B model is the smallest option; the repository recommends starting with 4B for accuracy and documents larger hardware requirements. Kev is a candidate, not a proven drop-in for our taxonomy, so it receives the same held-out evaluation and audit requirements as Laya.

**Keep Jev optional.** Add a Jev adapter only when access and budget are approved. All three options remain behind the same interface so the detection pipeline does not depend on a particular provider.

## 3. Fallback LLM classifier prompt sketch

A local, open-weight structured-output LLM is the fallback for KAN-91 when rules are insufficient. The adapter validates the model response, adds `backend` and `model_version`, and converts any validation failure to `REVIEW`.

The canonical families come from `backend/app/detection/taxonomy.py`:

```text
MODEL, RETRIEVAL, AGENT_TOOL, PIPELINE, CONFIGURATION, PLATFORM
```

`UNKNOWN` is not a `FailureFamily`. When evidence is insufficient, both taxonomy fields are `null` and the verdict is `REVIEW`.

The canonical categories are:

```text
HALLUCINATION, INSTRUCTION_FAILURE, FORMAT_FAILURE, REASONING_FAILURE,
REFUSAL_ERROR, CONFIDENCE_MISMATCH, RETRIEVAL_MISS, IRRELEVANT_RETRIEVAL,
RERANKING_FAILURE, CONTEXT_POLLUTION, CONTEXT_OVERFLOW, CITATION_FAILURE,
PLANNING_FAILURE, TOOL_SELECTION_FAILURE, TOOL_ARGUMENT_FAILURE,
TOOL_EXECUTION_FAILURE, LOOP_FAILURE, PREMATURE_TERMINATION, CONTEXT_LOSS,
SCHEMA_FAILURE, DEPENDENCY_FAILURE, TIMEOUT, PROMPT_REGRESSION,
MODEL_REGRESSION, PARAMETER_REGRESSION, TOKEN_LIMIT_FAILURE,
INGESTION_FAILURE, STORAGE_FAILURE, EVALUATOR_FAILURE, QUEUE_FAILURE,
PROVIDER_OUTAGE
```

Prompt sketch:

```text
System:
You are the Failure Forensics DecisionGate classifier. Evaluate only the supplied
redacted execution evidence. Do not repeat secrets or personal data. Do not invent
missing evidence.

Choose verdict from PASS, FAIL, REVIEW.
Choose failure_family from the canonical family list or null.
Choose failure_category from the canonical category list or null.

Rules:
- PASS requires evidence that the checked behavior satisfies its contract.
- FAIL requires evidence of a specific failure.
- REVIEW is required when evidence is insufficient, contradictory, unsupported,
  outside the taxonomy, or confidence is below the configured threshold.
- When verdict is PASS or REVIEW because the cause is unknown, set both taxonomy
  fields to null.
- A non-null category must belong to the selected family.

Redacted input payload:
{payload}

Return only one JSON object with exactly these fields:
{
  "verdict": "PASS | FAIL | REVIEW",
  "failure_family": "canonical family | null",
  "failure_category": "canonical category | null",
  "confidence": 0.0,
  "review_required": true
}
```

The implementation must validate this output with a typed schema. `confidence` must be between 0 and 1, `review_required` must be `true` for `REVIEW`, and family/category combinations must match the canonical taxonomy. Prompt text alone is not a security or correctness boundary.

## 4. Decision

Recommend ADR-004 remain vendor-neutral: rules first, Laya evaluated first, Kev evaluated second, and a local structured-output LLM as the fallback implementation path. Jev is an optional future adapter. Accuracy, calibration, cost and latency remain unverified for Failure Forensics until KAN-126 measures them on the project benchmark.
