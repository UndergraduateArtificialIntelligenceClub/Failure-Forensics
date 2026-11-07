"""Constants and component keys for Failure Forensics benchmark workloads.

These keys normalize span step identifiers across the Failure Forensics
benchmark harness.
"""

from enum import Enum


class WorkloadAKeys(str, Enum):
    """Component keys for Workload A (Document Pipeline).

    Normalizes span step identifiers across the Failure Forensics benchmark harness.
    """

    EXTRACTION: str = "doc_extraction"
    CLASSIFICATION: str = "doc_classification"
    SUMMARIZATION: str = "doc_summarization"


class WorkloadBKeys(str, Enum):
    """Component keys for Workload B (RAG Application).

    Normalizes span step identifiers across the Failure Forensics benchmark harness.
    """

    QUERY_REWRITE: str = "query_rewrite"
    RETRIEVAL: str = "retrieval"
    RERANKING: str = "reranker"
    CONTEXT_BUILD: str = "context_builder"
    GENERATION: str = "generator"


class WorkloadCKeys(str, Enum):
    """Component keys for Workload C (Agent Application).

    Normalizes span step identifiers across the Failure Forensics benchmark harness.
    """

    PLANNER: str = "planner"
    TOOL_SELECTION: str = "tool_selector"
    TOOL_EXECUTION: str = "tool_executor"


__all__ = [
    "WorkloadAKeys",
    "WorkloadBKeys",
    "WorkloadCKeys",
]
