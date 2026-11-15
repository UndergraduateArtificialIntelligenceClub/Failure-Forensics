"""Runnable version of the Blueprint v1.1 section 7.2 example."""

from failure_forensics import Forensics, InMemoryExporter

exporter = InMemoryExporter()
ff = Forensics(project="rag-demo", exporter=exporter)


@ff.trace(name="answer_question", pipeline_version="rag-v3")
def answer_question(question: str) -> str:
    with ff.span(
        "retrieve",
        type="retrieval",
        component="rag.retriever",
        input={"query": question},
    ) as retrieve:
        docs = ["AI reliability engineering", "OpenTelemetry tracing"]
        retrieve.set_output({"documents": docs})

    with ff.span(
        "generate",
        type="llm",
        component="rag.generator",
        inputs_from=[retrieve],
    ) as generate:
        answer = f"Answer based on {len(docs)} documents."
        generate.set_output({"answer": answer})

    return answer


if __name__ == "__main__":
    answer_question("How do we track AI failures?")
    print(exporter.traces[0])
