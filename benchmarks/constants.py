"""Standardized component keys for Failure Forensics benchmark workloads."""

from enum import Enum


class WorkloadAKeys(str, Enum):
    EXTRACTION = "doc.extraction"
    CLASSIFICATION = "doc.classification"
    SUMMARIZATION = "doc.summarization"


class WorkloadBKeys(str, Enum):
    QUERY_REWRITE = "rag.query_rewrite"
    RETRIEVAL = "rag.retriever"
    RERANKING = "rag.reranker"
    CONTEXT_BUILD = "rag.context_builder"
    GENERATION = "rag.generator"


class WorkloadCKeys(str, Enum):
    PLANNER = "agent.planner"
    TOOL_SELECTION = "agent.tool_selector"
    TOOL_EXECUTION = "agent.tool_executor"
    OBSERVATION = "agent.observation"
    REASONING = "agent.reasoning"
