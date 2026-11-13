import os
from failure_forensics import Forensics

# Initialize the client 
ff = Forensics(project='rag-demo', api_key=os.environ.get('FF_API_KEY', 'test-key'))

# Mock objects to stand in for the blueprint's retriever and llm placeholders
class MockRetriever:
    def search(self, query):
        return ["Doc 1: AI reliability engineering", "Doc 2: OTel tracing"]

class MockLLM:
    def generate(self, question, docs):
        return "Generated answer based on retrieved documents."

retriever = MockRetriever()
llm = MockLLM()

@ff.trace(name='answer_question')
def answer_question(question: str):
    with ff.span('retrieve', type='retrieval', input={'query': question}) as span:
        docs = retriever.search(question)
        span.set_output({'documents': docs})
    
    with ff.span('generate', type='llm', inputs_from=['retrieve']) as span:
        answer = llm.generate(question, docs)
        span.set_output({'answer': answer})
        
    return answer

if __name__ == "__main__":
    answer_question("How do we track AI failures?")
