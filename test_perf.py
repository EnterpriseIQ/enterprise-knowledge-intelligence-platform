import time

from src.pipeline import RAGPipeline
from src.retrieval.query_expansion import QueryExpander


class MockExpander(QueryExpander):
    def expand(self, query):
        return [query + f" {i}" for i in range(10)]

def run_benchmark():
    # Let's use the RAGPipeline as it properly sets up the dependencies
    pipeline = RAGPipeline()
    pipeline.build_index()

    # Modify the retriever to use the MockExpander
    pipeline.retriever.expander = MockExpander()

    start_time = time.time()
    for _ in range(20):
        # The query string itself doesn't matter much as it's the retrieval loop we are testing
        from src.retrieval.hybrid_retriever import RetrievalRequest
        req = RetrievalRequest(query="What is the remote work policy?", role="HR")
        pipeline.retriever.retrieve(req)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time taken: {duration:.4f} seconds")
    return duration

if __name__ == "__main__":
    run_benchmark()
