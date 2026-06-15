import time
from src.pipeline import RAGPipeline
from evaluation.metrics import precision_at_k, recall_at_k, mrr_at_k, ndcg_at_k

def run_benchmarks():
    pipeline = RAGPipeline()
    pipeline.build_index()

    # A tiny dummy dataset to verify the pipeline
    test_cases = [
        {
            "query": "What is the remote work policy?",
            "relevant_ids": {"hr-remote"},
            "role": "HR"
        },
        {
            "query": "Show engineering deployment standards",
            "relevant_ids": {"eng-deploy"},
            "role": "Engineering"
        }
    ]

    results = []

    for tc in test_cases:
        start_time = time.time()
        res = pipeline.query(tc["query"], role=tc["role"])
        latency = time.time() - start_time

        # We need chunk parent doc IDs to match our relevance labels
        retrieved_doc_ids = [c["doc_id"] for c in res.citations if "doc_id" in c]

        # Calculate metrics
        p_at_3 = precision_at_k(retrieved_doc_ids, tc["relevant_ids"], 3)
        r_at_3 = recall_at_k(retrieved_doc_ids, tc["relevant_ids"], 3)
        mrr = mrr_at_k(retrieved_doc_ids, tc["relevant_ids"], 3)
        ndcg = ndcg_at_k(retrieved_doc_ids, tc["relevant_ids"], 3)

        results.append({
            "query": tc["query"],
            "latency": latency,
            "precision@3": p_at_3,
            "recall@3": r_at_3,
            "mrr": mrr,
            "ndcg": ndcg,
            "confidence": res.confidence.get("score", 0.0)
        })

    return results

def write_report(results):
    avg_mrr = sum(r['mrr'] for r in results) / len(results)
    avg_ndcg = sum(r['ndcg'] for r in results) / len(results)
    avg_p3 = sum(r['precision@3'] for r in results) / len(results)
    avg_r3 = sum(r['recall@3'] for r in results) / len(results)
    avg_latency = sum(r['latency'] for r in results) / len(results)

    report_content = f"""# KnowledgeX Auto-Generated Benchmark Report

## Retrieval Quality
| Metric | Value |
| ------ | ----- |
| Mean Reciprocal Rank (MRR@3) | {avg_mrr:.2f} |
| NDCG@3 | {avg_ndcg:.2f} |
| Precision@3 | {avg_p3:.2f} |
| Recall@3 | {avg_r3:.2f} |

## System Performance
| Metric | Value |
| ------ | ----- |
| Average Latency (End-to-End) | {avg_latency:.2f}s |
"""
    with open("reports/benchmark_report.md", "w") as f:
        f.write(report_content)
    print("Report generated at reports/benchmark_report.md")

if __name__ == "__main__":
    results = run_benchmarks()
    write_report(results)
