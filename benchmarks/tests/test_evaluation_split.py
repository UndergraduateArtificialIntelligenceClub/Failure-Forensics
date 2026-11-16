import pytest

from benchmarks.evaluation_split import EvaluationCase, _rank, assign_splits


def _cases() -> list[EvaluationCase]:
    return [
        EvaluationCase(f"rerank-{seed}", "rag", "reranker_demotes", seed)
        for seed in range(10)
    ]


def test_split_is_deterministic_and_order_independent() -> None:
    cases = _cases()
    assert assign_splits(cases) == assign_splits(reversed(cases))


def test_split_is_stratified_by_fault_type() -> None:
    cases = [
        EvaluationCase("a-1", "rag", "fault-a", 1),
        EvaluationCase("a-2", "rag", "fault-a", 2),
        EvaluationCase("b-1", "rag", "fault-b", 1),
        EvaluationCase("b-2", "rag", "fault-b", 2),
    ]
    result = assign_splits(cases)

    assert {result["a-1"], result["a-2"]} == {"dev", "heldout"}
    assert {result["b-1"], result["b-2"]} == {"dev", "heldout"}


def test_fault_seed_is_part_of_the_stable_rank() -> None:
    original = EvaluationCase("same-id", "rag", "same-fault", 1)
    changed = EvaluationCase("same-id", "rag", "same-fault", 2)

    assert _rank(original, "project-seed") != _rank(changed, "project-seed")


def test_duplicate_case_ids_are_rejected() -> None:
    case = EvaluationCase("duplicate", "rag", "fault", 1)
    with pytest.raises(ValueError, match="duplicate case_id"):
        assign_splits([case, case])
