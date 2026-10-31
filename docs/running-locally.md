# Running Locally

!!! warning "Work in progress"
    The code lands from Sprint 1. Commands below are the target setup from the blueprint and are kept up to date by T3 (KAN-22, KAN-57).

## Requirements

- Python 3.12
- Node.js LTS
- Docker and Docker Compose
- Git, `make` (optional)
- One LLM provider key (OpenAI) for judges and the explainer

## Steps

```bash
git clone https://github.com/UndergraduateArtificialIntelligenceClub/Failure-Forensics.git
cd Failure-Forensics
cp .env.example .env              # fill in FF_OPENAI_API_KEY etc.

docker compose up -d              # PostgreSQL, Redis, MinIO
make migrate                      # alembic upgrade head
make seed                         # demo project, API key, 50 traces

make api                          # FastAPI on http://localhost:8000
make worker                       # Celery worker
make web                          # Next.js console on http://localhost:3000
```

## Send a first trace

```python
import os
from failure_forensics import Forensics

ff = Forensics(project="rag-demo", api_key=os.environ["FF_API_KEY"])

@ff.trace(name="answer_question", pipeline_version="rag-v3")
def answer_question(question: str) -> str:
    with ff.span("retrieve", type="retrieval", component="rag.retriever",
                 input={"query": question}) as retrieve:
        docs = retriever.search(question)
        retrieve.set_output({"documents": docs})

    with ff.span("generate", type="llm", component="rag.generator",
                 inputs_from=[retrieve]) as generate:
        answer = llm.generate(question, docs)
        generate.set_output({"answer": answer})

    return answer
```

## Run the benchmarks

```bash
make bench-doc        # benchmark A
make bench-rag        # benchmark B
make bench-agent      # benchmark C
make eval-dev         # accuracy on the dev split
```

## Build these docs

```bash
pip install -r requirements-docs.txt
mkdocs serve          # http://127.0.0.1:8000
```
