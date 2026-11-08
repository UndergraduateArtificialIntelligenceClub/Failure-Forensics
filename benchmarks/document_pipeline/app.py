import json
from pathlib import Path
from benchmarks.constants import WorkloadAKeys

def extract_text(raw_text: str) -> dict:
    cleaned_text = " ".join(raw_text.split())
    return {
        "step_key": WorkloadAKeys.EXTRACTION.value,
        "input_text": raw_text,
        "cleaned_text": cleaned_text,
    }

def classify_text(cleaned_text: str) -> dict:
    text_lower = cleaned_text.lower()
    if any(k in text_lower for k in ["billing", "invoice", "charge", "credit"]):
        category = "Billing"
    elif any(k in text_lower for k in ["error", "bug", "issue", "tier"]):
        category = "Technical"
    elif any(k in text_lower for k in ["policy", "compliance"]):
        category = "Policy"
    else:
        category = "General"
        
    return {
        "step_key": WorkloadAKeys.CLASSIFICATION.value,
        "cleaned_text": cleaned_text,
        "predicted_category": category,
    }

def summarize_text(cleaned_text: str) -> dict:
    sentences = [s.strip() for s in cleaned_text.split(".") if s.strip()]
    summary = ". ".join(sentences[:2]) + ("." if sentences else "")
    return {
        "step_key": WorkloadAKeys.SUMMARIZATION.value,
        "cleaned_text": cleaned_text,
        "generated_summary": summary,
    }

def run_pipeline(doc_fixture: dict) -> dict:
    ext_res = extract_text(doc_fixture.get("text", ""))
    cls_res = classify_text(ext_res["cleaned_text"])
    sum_res = summarize_text(ext_res["cleaned_text"])
    
    return {
        "doc_id": doc_fixture.get("id"),
        "steps": {
            WorkloadAKeys.EXTRACTION.value: ext_res,
            WorkloadAKeys.CLASSIFICATION.value: cls_res,
            WorkloadAKeys.SUMMARIZATION.value: sum_res,
        },
        "predicted_category": cls_res["predicted_category"],
        "generated_summary": sum_res["generated_summary"],
    }

if __name__ == "__main__":
    dataset_path = Path(__file__).parent.parent / "datasets" / "document_samples.json"
    with open(dataset_path, "r", encoding="utf-8") as f:
        docs = json.load(f)
        
    results = [run_pipeline(doc) for doc in docs]
    print(json.dumps(results, indent=2))
