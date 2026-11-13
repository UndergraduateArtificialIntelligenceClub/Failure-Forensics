"""Standardized component keys for Failure Forensics benchmark workloads."""

from enum import Enum


class WorkloadAKeys(str, Enum):
    EXTRACTION = "doc_extraction"
    CLASSIFICATION = "doc_classification"
    SUMMARIZATION = "doc_summarization"


class WorkloadBKeys(str, Enum):
    QUERY_REWRITE = "query_rewrite"
    RETRIEVAL = "retrieval"
    RERANKING = "reranker"
    CONTEXT_BUILD = "context_builder"
    GENERATION = "generator"


class WorkloadCKeys(str, Enum):
    PLANNER = "planner"
    TOOL_SELECTION = "tool_selector"
    TOOL_EXECUTION = "tool_executor"
    OBSERVATION = "observation"
    REASONING = "reasoning"
