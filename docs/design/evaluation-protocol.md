# Evaluation Protocol (Draft)

- **Ticket:** KAN-33 (Sprint 1)
- **Status:** Draft — Input to ADR-007 (`KAN-72`)
- **Owner:** T7 (Evaluation & Benchmarks)

This document defines the quantitative evaluation metrics (§2.5), deterministic `dev` / `held-out` dataset partitioning rules, and governance constraints for benchmarking the Failure Forensics root-cause analysis (RCA) engine across Workloads A (Document), B (RAG), and C (Agent).

---

## 1. Evaluation Dataset Partitioning

Each benchmark workload generates three distinct evaluation sets:

1. **Fault-injected traces ($T_{\text{fail}}$):** Executions with a single known ground-truth fault injected at a target `component_key` and labeled with a two-level `(family, category)` taxonomy label.
2. **Clean baseline traces ($T_{\text{healthy}}$):** Unperturbed executions of the same benchmark workloads with no injected faults.
3. **Regression replay cases ($R$):** Previously failing traces (from synthetic faults or human-confirmed production reviews) paired with a configuration, prompt, or code fix and an invariant assertion suite.

---

## 2. Evaluation Metrics (§2.5)

### 2.1 Top-1 Root-Cause Accuracy

Measures how often the engine's highest-ranked root-cause candidate matches the true fault origin on fault-injected traces ($T_{\text{fail}}$).

$$\text{Top-1 Accuracy} = \frac{1}{|T_{\text{fail}}|} \sum_{t \in T_{\text{fail}}} \mathbb{I}\left(\hat{c}_1(t) = c^*(t)\right)$$

- **Matching rule:** Evaluated on canonical `component_key` (e.g., `rag.reranker`) rather than ephemeral `span_id` so multi-attempt or retried spans map consistently to the responsible pipeline stage.
- **Tie-breaking:** Candidates with identical ranking scores ($\text{severity} \times \text{confidence} \times \text{earliness}$) are ordered deterministically by causal topological order (earliest span first), then lexicographically by `component_key`.

### 2.2 Top-3 Root-Cause Accuracy

Measures whether the ground-truth faulty component appears anywhere within the engine's top three ranked root-cause candidates.

$$\text{Top-3 Accuracy} = \frac{1}{|T_{\text{fail}}|} \sum_{t \in T_{\text{fail}}} \mathbb{I}\left(c^*(t) \in \{\hat{c}_1(t), \hat{c}_2(t), \hat{c}_3(t)\}\right)$$

- **Rule:** If the engine emits fewer than three candidates, membership is checked over the returned list without padding.

### 2.3 Failure Classification Macro-F1

Measures balanced classification accuracy across all failure categories in `taxonomy.py` without letting frequent fault types mask poor performance on rarer ones.

$$\text{Macro-F1} = \frac{1}{|K|} \sum_{k \in K} \frac{2 \cdot \text{Precision}_k \cdot \text{Recall}_k}{\text{Precision}_k + \text{Recall}_k}$$

- **Granularity:** Computed at the leaf **category** level (29 categories across the 6 families defined in `architecture.md`), with family-level Macro-F1 reported as a secondary diagnostic breakdown.
- **Zero-support handling:** Categories with zero ground-truth instances in a given evaluation slice ($|T_k| = 0$) are excluded from the denominator $|K|$ for that run rather than scored as $0$.

### 2.4 Evidence Grounding Rate

Measures how reliably the diagnosis explainer anchors its claims in stored trace evidence (`EvidenceRef`) prior to enforcement by the grounding gate (per `docs/design/evidence-model.md`).

$$\text{Evidence Grounding Rate} = \frac{N_{\text{supported}} + N_{\text{inference}}}{N_{\text{claims\_written}}}$$

- **Pre-gate measurement:** Counted across all claims emitted by the explainer **before** the grounding gate strips or flags unsupported claims (measuring post-gate would trivially yield 100%).
- **Validity requirement:** A claim counts as grounded only if its cited `EvidenceRef` resolves to a stored trace span/signal in the current trace and its content hash matches the persisted record.

### 2.5 False Positive Rate (FPR)

Measures how often the engine wrongly flags healthy executions as failed.

$$\text{False Positive Rate} = \frac{1}{|T_{\text{healthy}}|} \sum_{t \in T_{\text{healthy}}} \mathbb{I}\left(\text{predicted\_status}(t) = \texttt{failed}\right)$$

- **Rule:** Evaluated strictly over clean baseline traces ($T_{\text{healthy}}$). Both an explicit `failed` status verdict and an unprompted root-cause diagnosis on a clean trace count as a false positive.

### 2.6 Diagnosis Latency

Measures end-to-end analysis speed from worker execution start to persistence of the final `Diagnosis` record.

$$\text{Latency}_t = t_{\text{diagnosis\_completed}} - t_{\text{worker\_started}}$$

- **Reporting:** Reported in milliseconds (`ms`) as **p50 (median)** and **p95 (95th percentile)** across all completed evaluation traces.
- **Queue separation & timeouts:** Queue wait time ($t_{\text{worker\_started}} - t_{\text{enqueued}}$) is logged separately so background worker saturation does not distort engine latency. Jobs exceeding the worker timeout threshold are counted separately as timeout failures rather than clipped into percentiles.

### 2.7 Regression Pass Rate

Measures whether a remediation resolves a known failure without introducing regressions on previously passing checks.

$$\text{Regression Pass Rate} = \frac{1}{|R|} \sum_{r \in R} \mathbb{I}\left(\text{target\_fixed}(r) \land \text{no\_new\_failures}(r)\right)$$

- **All-or-nothing grading:** Each replay case $r \in R$ passes (`1`) if and only if the original root-cause signal clears **and** all baseline assertions remain green. Partial fixes score `0`.

### 2.8 Human Override Rate

Measures how often human reviewers reject or correct automated verdicts during trace triage.

$$\text{Human Override Rate} = \frac{1}{|D_{\text{reviewed}}|} \sum_{d \in D_{\text{reviewed}}} \mathbb{I}\left(\text{overridden}(d) = \texttt{true}\right)$$

- **Denominator:** Computed strictly over diagnoses inspected by a human reviewer ($D_{\text{reviewed}}$), excluding unreviewed diagnoses.
- **Override criteria:** Triggered when a reviewer modifies the root-cause `component_key`, failure `category`, or overall failure `status` (via the review correction workflow). Purely stylistic edits to free-text explanation prose do not count as overrides.

---

## 3. Deterministic Dev / Held-Out Split Rule

To prevent prompt, threshold, or rule overfitting while keeping benchmark splits reproducible across contributors, all synthetic and curated benchmark cases are partitioned deterministically by **fault type** and **seed**.

### 3.1 Stratification and Ratio

- **Stratification key:** `(workload, failure_family, failure_category)` for fault-injected cases, and `(workload, "HEALTHY")` for clean baseline cases.
- **Target split ratio:** **70% `dev` / 30% `held-out`** within each stratum.
- **Minimum coverage:** Every populated `(workload, failure_category)` stratum with $\ge 2$ cases must allocate at least 1 case to `held-out`.

### 3.2 Deterministic Assignment Algorithm

Splits are assigned per case via cryptographic hashing of a fixed project seed (`SPLIT_SEED = "failure-forensics-v1-2026"`) and the case's immutable `case_id` (e.g., `doc_002_schema_01`):

```python
import hashlib


def assign_split(case_id: str, seed: str = "failure-forensics-v1-2026", dev_ratio: float = 0.70) -> str:
    digest = hashlib.sha256(f"{seed}:{case_id}".encode("utf-8")).digest()
    bucket = int.from_bytes(digest[:8], "big") / (1 << 64)
    return "dev" if bucket < dev_ratio else "held-out"
```

- **Why hash-bucketing over global list shuffling:** Adding new cases to one workload or fault category never shifts existing `case_id` assignments between `dev` and `held-out`.
- **Manifest persistence:** Generated split assignments are frozen in versioned dataset manifests (`datasets/<workload>/manifest.json`) with `split`, `fault_family`, `fault_category`, and `seed` recorded per case.

### 3.3 Leakage Prevention Governance

1. **`dev` split:** Open for iterative development, rule/judge prompt tuning, and CI regression checks across Sprints 2–7.
2. **`held-out` split:** Sealed during development. Prompts, heuristics, and thresholds may not be tuned against `held-out` error cases.
3. **Single-run execution:** The `held-out` suite is executed **once** in Sprint 8 (`KAN-127`) and reported directly in the final evaluation report (`KAN-140`).

---

## 4. Inputs to ADR-007 (`KAN-72`)

This draft supplies the following specifications for formal ratification in **ADR-007 (Evaluation Methodology)** during Sprint 4:

| Decision Area | Proposed Protocol Default | Stakeholders |
|---|---|---|
| **Primary Accuracy Metrics** | Top-1 & Top-3 on canonical `component_key`; leaf-category Macro-F1 | T5, T7 |
| **Grounding Rate Formula** | Pre-gate `(supported + inference) / total_claims_written` | T1, T5, T7 |
| **Split Ratio & Seed** | 70/30 `dev`/`held-out` stratified by `(workload, category)` via SHA-256 hash bucketing (`SPLIT_SEED = "failure-forensics-v1-2026"`) | T1, T7 |
| **Latency Measurement** | Worker execution duration (`p50`, `p95` in `ms`), isolated from queue wait time | T3, T7 |
| **Held-Out Governance** | Single-run freeze until Sprint 8 (`KAN-127`) | T1, T5, T7 |