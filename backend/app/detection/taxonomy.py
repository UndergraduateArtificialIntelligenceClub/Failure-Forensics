"""
Failure Forensics Taxonomy Module v1 (KAN-26)
Matches Section 9 of the Technical Architecture & Engineering Blueprint [cite: 21].
"""

from enum import Enum


class FailureFamily(str, Enum):
    MODEL = "Model"
    RETRIEVAL_RAG = "Retrieval/RAG"
    AGENT_TOOL = "Agent/Tool"
    PIPELINE = "Pipeline"
    CONFIGURATION = "Configuration"
    PLATFORM = "Platform"


class FailureCategory(str, Enum):
    # Model Failures
    HALLUCINATION = "HALLUCINATION"  # Model generates unsupported or factually incorrect assertions.
    INSTRUCTION_FAILURE = "INSTRUCTION_FAILURE"  # Model fails to follow explicit prompt instructions or constraints.
    FORMAT_FAILURE = "FORMAT_FAILURE"  # Model output format does not match expected schema or structure.
    REASONING_FAILURE = "REASONING_FAILURE"  # Model logic or chain-of-thought contains flaws or invalid steps.
    REFUSAL_ERROR = "REFUSAL_ERROR"  # Model inappropriately refuses a valid prompt or query.
    CONFIDENCE_MISMATCH = "CONFIDENCE_MISMATCH"  # Model confidence level does not align with output correctness.
    
    # Retrieval/RAG Failures
    RETRIEVAL_MISS = "RETRIEVAL_MISS"  # System failed to retrieve the necessary document or knowledge source.
    IRRELEVANT_RETRIEVAL = "IRRELEVANT_RETRIEVAL"  # Retrieved documents fail to contain the required context.
    RERANKING_FAILURE = "RERANKING_FAILURE"  # Reranking step degraded the ranking of relevant context.
    CONTEXT_POLLUTION = "CONTEXT_POLLUTION"  # Retrieved context includes noise, irrelevant data, or conflicting facts.
    CONTEXT_OVERFLOW = "CONTEXT_OVERFLOW"  # Retrieval assembled too much text for effective context windows.
    CITATION_FAILURE = "CITATION_FAILURE"  # Generated response fails to cite sources correctly or cites wrong contexts.
    
    # Agent/Tool Failures
    PLANNING_FAILURE = "PLANNING_FAILURE"  # Agent fails to construct a valid multi-step plan to achieve the goal.
    TOOL_SELECTION_FAILURE = "TOOL_SELECTION_FAILURE"  # Agent selected an inappropriate tool for the objective.
    TOOL_ARGUMENT_FAILURE = "TOOL_ARGUMENT_FAILURE"  # Tool invoked with invalid, malformed, or missing arguments.
    TOOL_EXECUTION_FAILURE = "TOOL_EXECUTION_FAILURE"  # Tool invocation failed with runtime exceptions or errors.
    LOOP_FAILURE = "LOOP_FAILURE"  # Agent entered a repetitive execution cycle without making progress.
    PREMATURE_TERMINATION = "PREMATURE_TERMINATION"  # Agent stopped execution before completing the task.
    
    # Pipeline Failures
    CONTEXT_LOSS = "CONTEXT_LOSS"  # Essential context or state dropped between pipeline execution steps.
    PROPAGATION_ERROR = "PROPAGATION_ERROR"  # Downstream step corrupted or incorrectly handled upstream data.
    SCHEMA_FAILURE = "SCHEMA_FAILURE"  # Pipeline contract violation between consecutive step interfaces.
    DEPENDENCY_FAILURE = "DEPENDENCY_FAILURE"  # Step failed due to an unavailable external dependency or service.
    TIMEOUT = "TIMEOUT"  # Step execution exceeded maximum allowable duration.
    
    # Configuration Failures
    PROMPT_REGRESSION = "PROMPT_REGRESSION"  # Prompt change introduced unexpected behavioral regressions.
    MODEL_REGRESSION = "MODEL_REGRESSION"  # Model version update introduced behavioral regressions.
    PARAMETER_REGRESSION = "PARAMETER_REGRESSION"  # Hyperparameter or configuration change degraded performance.
    TOKEN_LIMIT_FAILURE = "TOKEN_LIMIT_FAILURE"  # Execution hit token limit constraints or truncation thresholds.
    
    # Platform Failures
    INGESTION_FAILURE = "INGESTION_FAILURE"  # Failure while recording or ingesting traces, spans, or signals.
    STORAGE_FAILURE = "STORAGE_FAILURE"  # Database, object storage, or persistence layer failure.
    EVALUATOR_FAILURE = "EVALUATOR_FAILURE"  # Evaluation runner or scoring component encountered an error.
    QUEUE_FAILURE = "QUEUE_FAILURE"  # Message queue or asynchronous processing failure (Celery/Redis).
    PROVIDER_OUTAGE = "PROVIDER_OUTAGE"  # External AI provider or service outage.
