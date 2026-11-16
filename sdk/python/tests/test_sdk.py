import runpy
from pathlib import Path

import pytest

from failure_forensics import Forensics, InMemoryExporter


def test_decorator_spans_and_inputs_from_link() -> None:
    exporter = InMemoryExporter()
    ff = Forensics("test-project", exporter=exporter)

    @ff.trace("pipeline", pipeline_version="v1")
    def pipeline() -> str:
        with ff.span("first", component="rag.retriever") as first:
            first.set_output({"documents": ["one"]})
        with ff.span(
            "second", component="rag.generator", inputs_from=[first]
        ) as second:
            second.set_output({"answer": "done"})
        return "done"

    assert pipeline() == "done"
    trace = exporter.traces[0]
    assert trace["status"] == "ok"
    assert trace["pipeline_version"] == "v1"
    assert len(trace["trace_id"]) == 32
    assert [span["component_key"] for span in trace["spans"]] == [
        "rag.retriever",
        "rag.generator",
    ]
    assert trace["links"] == [
        {
            "from_span_id": trace["spans"][0]["span_id"],
            "to_span_id": trace["spans"][1]["span_id"],
            "relation": "consumes_output_of",
        }
    ]


def test_nested_spans_record_parent_and_child() -> None:
    exporter = InMemoryExporter()
    ff = Forensics("test-project", exporter=exporter)

    @ff.trace("nested")
    def nested() -> None:
        with ff.span("parent"), ff.span("child"):
            pass

    nested()
    child, parent = exporter.traces[0]["spans"]
    assert child["parent_span_id"] == parent["span_id"]


def test_exception_marks_span_and_trace_then_reraises() -> None:
    exporter = InMemoryExporter()
    ff = Forensics("test-project", exporter=exporter)

    @ff.trace("failure")
    def failure() -> None:
        with ff.span("broken"):
            raise ValueError("bad output")

    with pytest.raises(ValueError, match="bad output"):
        failure()

    trace = exporter.traces[0]
    assert trace["status"] == "error"
    assert trace["error"]["type"] == "ValueError"
    assert trace["spans"][0]["status"] == "error"


def test_span_requires_an_active_trace() -> None:
    ff = Forensics("test-project")
    with pytest.raises(RuntimeError, match="inside an @trace"), ff.span("orphan"):
        pass


def test_blueprint_example_runs_with_stub_exporter() -> None:
    example = Path(__file__).parents[1] / "examples" / "rag_demo.py"
    namespace = runpy.run_path(str(example), run_name="test_example")
    namespace["answer_question"]("question")

    trace = namespace["exporter"].traces[0]
    assert trace["status"] == "ok"
    assert len(trace["links"]) == 1
