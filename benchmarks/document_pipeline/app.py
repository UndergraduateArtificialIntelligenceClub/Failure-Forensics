"""Benchmark A: Document processing pipeline.

Executes sequential extraction, classification, and summarization steps
normalized across the Failure Forensics benchmark harness.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

# Ensure repository root is in sys.path for direct execution
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from benchmarks.constants import WorkloadAKeys

_CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Billing": ("billing", "invoice", "charge", "payment", "fee", "credit", "subscription"),
    "Technical": ("error", "bug", "gateway", "api", "release", "timeout", "endpoint", "proxy", "tls", "streaming", "changelog"),
    "Policy": ("policy", "encryption", "compliance", "non-compliant", "access", "posture"),
    "Account": ("account", "admin", "tenant", "organization", "deprovisioning", "ownership", "profile"),
}


def extract_text(raw_text: str) -> dict[str, Any]:
    """Normalizes whitespace and strips trailing spaces.

    Args:
        raw_text: The input text payload.

    Returns:
        Dictionary containing step_key, input_text, and cleaned_text.
    """
    cleaned_text = re.sub(r"\s+", " ", raw_text).strip()
    return {
        "step_key": WorkloadAKeys.EXTRACTION.value,
        "input_text": raw_text,
        "cleaned_text": cleaned_text,
    }


def classify_text(cleaned_text: str) -> dict[str, Any]:
    """Inspects the cleaned text for simple keywords to infer a category label.

    If no keyword matches, returns "General".

    Args:
        cleaned_text: Normalized document text.

    Returns:
        Dictionary containing step_key, cleaned_text, and predicted_category.
    """
    text_lower = cleaned_text.lower()
    predicted_category = "General"

    for category, keywords in _CATEGORY_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            predicted_category = category
            break

    return {
        "step_key": WorkloadAKeys.CLASSIFICATION.value,
        "cleaned_text": cleaned_text,
        "predicted_category": predicted_category,
    }


def summarize_text(cleaned_text: str) -> dict[str, Any]:
    """Extracts key sentences to create a concise 1-2 sentence representation.

    Args:
        cleaned_text: Normalized document text.

    Returns:
        Dictionary containing step_key, cleaned_text, and generated_summary.
    """
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned_text) if s.strip()]
    generated_summary = " ".join(sentences[:2]) if sentences else cleaned_text

    return {
        "step_key": WorkloadAKeys.SUMMARIZATION.value,
        "cleaned_text": cleaned_text,
        "generated_summary": generated_summary,
    }


def run_pipeline(doc_fixture: dict[str, Any]) -> dict[str, Any]:
    """Sequentially executes extraction -> classification -> summarization.

    Args:
        doc_fixture: Document dictionary containing id, text, etc.

    Returns:
        Consolidated pipeline result containing doc_id, individual step outputs,
        and final results (predicted_category, generated_summary).
    """
    doc_id = doc_fixture.get("id", "unknown_doc")
    raw_text = doc_fixture.get("text", "")

    extraction_output = extract_text(raw_text)
    cleaned_text = extraction_output["cleaned_text"]

    classification_output = classify_text(cleaned_text)
    summarization_output = summarize_text(cleaned_text)

    return {
        "doc_id": doc_id,
        "steps": {
            WorkloadAKeys.EXTRACTION.value: extraction_output,
            WorkloadAKeys.CLASSIFICATION.value: classification_output,
            WorkloadAKeys.SUMMARIZATION.value: summarization_output,
        },
        "predicted_category": classification_output["predicted_category"],
        "generated_summary": summarization_output["generated_summary"],
    }


if __name__ == "__main__":
    dataset_path = Path(__file__).resolve().parent.parent / "datasets" / "document_samples.json"
    with open(dataset_path, "r", encoding="utf-8") as f:
        samples = json.load(f)

    if samples:
        result = run_pipeline(samples[0])
        print(json.dumps(result, indent=2))
