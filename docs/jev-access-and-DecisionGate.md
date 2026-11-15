# KAN-27: Jev Access Investigation & DecisionGate Recommendation

## 1. Jev Investigation (What Jev is, API, Cost, & Latency)

- **What Jev is:** Jev (by TypeSafe AI) is a specialized, non-prose decision-routing and classification model designed to take an execution state or payload and return typed, calibrated choices or probabilities rather than free-form text.
- **Access & API Status:** Team access and API credentials are currently **unapproved and unavailable**. Direct TypeSafe console signups have been waitlist-gated/paused, and no shared team API key or third-party gateway budget (e.g., OpenRouter/Vercel) has been provisioned.
- **Cost & Latency:** Publicly cited benchmarks indicate low token pricing for routing workloads (~$0.042 per 1M input tokens), but actual production latency, rate limits, and end-to-end pipeline costs remain unverified due to lack of live credentials.
- **Impact:** Jev cannot block the M0 architecture freeze or MVP delivery. Per Blueprint Errata E3/E4, it is relegated strictly to an optional future adapter (**KAN-103**) contingent on future team approval.

---

## 2. Recommendation for ADR-004

To avoid blocking the MVP on an unapproved external API, adopt a vendor-neutral `DecisionGate.decide(decision_type, payload)` interface backed by deterministic rules first and self-hosted open-source models second:

1. **Primary Candidate — Laya Typed-Decisions (421M parameters, Apache 2.0):**
   - _License & Runtime:_ Permissive Apache 2.0 license with zero licensing fees and a lightweight local footprint suitable for self-hosted inference.
   - _Recommendation:_ Evaluate first against Failure Forensics' specific taxonomy and held-out failure fixtures before production adoption.
2. **Secondary Candidate — Kev (0.8B and 4B parameters, Apache 2.0):**
   - _License & Runtime:_ Permissive Apache 2.0 license, self-hostable local decision model.
   - _Recommendation:_ Retain as the immediate fallback candidate if Laya's task fit, probability calibration, or output mapping proves unsuitable.

---

## 3. Fallback LLM Classifier Prompt Sketch

Behind the `DecisionGate` interface, a local, open-weight LLM classifier serves as the swappable fallback when deterministic rules are insufficient (implementation path for **KAN-91**):

- **Routing & Safety Rules:**
  - Must enforce project capture/redaction policies (no unredacted PII or secrets persisted in decision logs).
  - Must classify into the v1.1 taxonomy families (`MODEL`, `RETRIEVAL`, `AGENT_TOOL`, `PIPELINE`, `CONFIGURATION`, `PLATFORM`, `UNKNOWN`) per Blueprint Errata E7.
  - Any invalid JSON output, backend error, or low-confidence score automatically defaults `verdict` to `REVIEW` and sets `review_required: true`.

- **Prompt Sketch:**

  ```text
  System: You are the Failure Forensics DecisionGate classifier. Analyze the provided execution span or quality signal payload. Do not log, echo, or retain unredacted PII or secrets.

  Classify the input strictly into one primary failure_family from the v1.1 taxonomy:
  [MODEL, RETRIEVAL, AGENT_TOOL, PIPELINE, CONFIGURATION, PLATFORM, UNKNOWN]

  Input Payload: {payload}

  Respond ONLY with valid JSON matching this exact schema:
  {
    "verdict": "PASS" | "FAIL" | "REVIEW",
    "failure_family": "<enum from list above>",
    "failure_category": "<specific category string or null>",
    "confidence": <float between 0.0 and 1.0>,
    "review_required": <boolean>
  }
  ```
