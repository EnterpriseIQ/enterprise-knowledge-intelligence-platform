import time

from src.retrieval.bm25_retriever import BM25Retriever


def run_benchmark():
    records = []
    # simulate a fairly large corpus
    for i in range(10000):
        records.append({"id": str(i), "text": f"some text with id {i} and content {i%10} {i%100} security enterprise test", "metadata": {}})

    start = time.time()
    bm25 = BM25Retriever(records)
    bm25._impl = None
    bm25._build_builtin()
    print("build time", time.time() - start)

    start_time = time.time()
    for _ in range(100):
        bm25.search("security enterprise test 5 50", k=10)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    run_benchmark()
