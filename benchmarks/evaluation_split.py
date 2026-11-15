"""Deterministic dev/held-out assignment for benchmark cases."""

from __future__ import annotations

import hashlib
import math
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass

SPLIT_SEED = "failure-forensics-v1-2026"


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    workload: str
    fault_type: str
    random_seed: int


def _rank(case: EvaluationCase, project_seed: str) -> bytes:
    value = (
        f"{project_seed}:{case.workload}:{case.fault_type}:"
        f"{case.random_seed}:{case.case_id}"
    )
    return hashlib.sha256(value.encode()).digest()


def assign_splits(
    cases: Iterable[EvaluationCase],
    *,
    project_seed: str = SPLIT_SEED,
    heldout_ratio: float = 0.30,
) -> dict[str, str]:
    """Assign cases within each workload/fault-type stratum.

    A stratum with at least two cases always has a held-out example. The result
    is independent of input ordering. Persist the result in the dataset manifest
    so later additions cannot move an existing case between splits.
    """
    if not 0 < heldout_ratio < 1:
        raise ValueError("heldout_ratio must be between 0 and 1")

    groups: dict[tuple[str, str], list[EvaluationCase]] = defaultdict(list)
    seen_ids: set[str] = set()
    for case in cases:
        if case.case_id in seen_ids:
            raise ValueError(f"duplicate case_id: {case.case_id}")
        seen_ids.add(case.case_id)
        groups[(case.workload, case.fault_type)].append(case)

    assignments: dict[str, str] = {}
    for group in groups.values():
        ordered = sorted(
            group, key=lambda case: (_rank(case, project_seed), case.case_id)
        )
        heldout_count = (
            0 if len(ordered) < 2 else max(1, math.ceil(len(ordered) * heldout_ratio))
        )
        heldout_ids = {case.case_id for case in ordered[:heldout_count]}
        assignments.update(
            {
                case.case_id: "heldout" if case.case_id in heldout_ids else "dev"
                for case in ordered
            }
        )
    return assignments
