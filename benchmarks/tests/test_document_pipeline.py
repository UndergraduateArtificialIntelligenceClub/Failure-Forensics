import pytest
from benchmarks.constants import WorkloadAKeys, WorkloadCKeys
from benchmarks.document_pipeline.app import (
    extract_text,
    classify_text,
    summarize_text,
    run_pipeline,
)

def test_agent_keys_exist():
    assert WorkloadCKeys.OBSERVATION.value == "observation"
    assert WorkloadCKeys.REASONING.value == "reasoning"

def test_extract_text():
    raw = "   Sample text   with   spaces.  "
    res = extract_text(raw)
    assert res["step_key"] == WorkloadAKeys.EXTRACTION.value
    assert res["cleaned_text"] == "Sample text with spaces."

def test_classify_text_billing():
    res = classify_text("This invoice has an issue with billing.")
    assert res["step_key"] == WorkloadAKeys.CLASSIFICATION.value
    assert res["predicted_category"] == "Billing"

def test_classify_text_fallback():
    res = classify_text("Random text without keywords.")
    assert res["predicted_category"] == "General"

def test_summarize_text():
    text = "First sentence. Second sentence. Third sentence."
    res = summarize_text(text)
    assert res["step_key"] == WorkloadAKeys.SUMMARIZATION.value
    assert res["generated_summary"] == "First sentence. Second sentence."

def test_run_pipeline_end_to_end():
    fixture = {
        "id": "doc_test",
        "text": "Billing invoice statement. Extra details here."
    }
    output = run_pipeline(fixture)
    assert output["doc_id"] == "doc_test"
    assert WorkloadAKeys.EXTRACTION.value in output["steps"]
    assert WorkloadAKeys.CLASSIFICATION.value in output["steps"]
    assert WorkloadAKeys.SUMMARIZATION.value in output["steps"]
    assert output["predicted_category"] == "Billing"
