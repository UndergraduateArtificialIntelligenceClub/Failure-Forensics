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

Measures how reliably the diagnosis explainer anchors its claims in stored trace evidence (`EvidenceRef`) after the grounding gate has checked them (per `docs/design/evidence-model.md`).

$$\text{Evidence Grounding Rate} = \frac{N_{\text{supported}} + N_{\text{inference}}}{N_{\text{claims\_written}}}$$

- **Denominator:** Includes every claim emitted before the gate. The numerator uses the gate's final `supported` or `inference` outcome, so deleting an unsupported claim cannot inflate the score.
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

### 2.9 Proposed Blueprint Targets

Targets are evaluated on the frozen held-out set: Top-1 $\ge 60\%$, Top-3 $\ge 85\%$, category Macro-F1 $\ge 0.70$, grounding $\ge 95\%$, false-positive rate $\le 10\%$, and p95 diagnosis latency $\le 60$ seconds. Human override rate and regression pass rate are reported without an initial threshold.

---

## 3. Deterministic Dev / Held-Out Split Rule

To prevent prompt, threshold, or rule overfitting while keeping benchmark splits reproducible across contributors, all synthetic and curated benchmark cases are partitioned deterministically by **fault type** and **seed**.

### 3.1 Stratification and Ratio

- **Stratification key:** `(workload, fault_type)` for fault-injected cases, and `(workload, "HEALTHY")` for clean baseline cases. This matches the `InjectedFault.fault_type` contract rather than grouping distinct injections that happen to share a taxonomy category.
- **Target split ratio:** **70% `dev` / 30% `held-out`** within each stratum.
- **Minimum coverage:** Every populated stratum with $\ge 2$ cases allocates at least 1 case to `held-out`.

### 3.2 Deterministic Assignment Algorithm

Within each stratum, cases are ranked by a SHA-256 digest of the fixed project seed, workload, fault type, the fault's `random_seed`, and immutable `case_id`. The first 30% (rounded up, with a minimum of one when the stratum has at least two cases) are held out. The executable reference is `benchmarks/evaluation_split.py`:

```python
assign_splits(
    [EvaluationCase(case_id, workload, fault_type, random_seed), ...],
    project_seed="failure-forensics-v1-2026",
    heldout_ratio=0.30,
)
```

- **Why deterministic ranking over global shuffling:** Input order cannot change the result, and each fault type receives held-out coverage instead of relying on chance.
- **Manifest persistence:** Generated assignments are frozen in versioned dataset manifests (`datasets/<workload>/manifest.json`) with `split`, `fault_type`, `failure_family`, `failure_category`, and `random_seed` recorded per case. New cases receive a split only when the manifest is deliberately regenerated and reviewed.

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
| **Grounding Rate Formula** | Gate-verified `(supported + inference) / total_claims_written`, retaining pre-gate claims in the denominator | T1, T5, T7 |
| **Split Ratio & Seed** | 70/30 `dev`/`held-out` stratified by `(workload, fault_type)` and ranked by project seed plus fault `random_seed` | T1, T7 |
| **Latency Measurement** | Worker execution duration (`p50`, `p95` in `ms`), isolated from queue wait time | T3, T7 |
| **Held-Out Governance** | Single-run freeze until Sprint 8 (`KAN-127`) | T1, T5, T7 |
