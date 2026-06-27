import random
import time
import uuid

from src.retrieval.rrf import reciprocal_rank_fusion

# We just want to measure the specific code section.

def run_benchmark():
    # Generate some fake data
    all_dense = []
    all_sparse = []

    num_queries = 20
    docs_per_query = 100

    # Pre-generate some doc IDs
    doc_ids = [str(uuid.uuid4()) for _ in range(500)]

    for _ in range(num_queries):
        query_dense = []
        query_sparse = []
        for i in range(docs_per_query):
            doc_id = random.choice(doc_ids)
            query_dense.append({
                "id": doc_id,
                "text": f"Dense doc {doc_id}",
                "metadata": {"source": "fake"},
                "semantic_score": random.random()
            })
            query_sparse.append({
                "id": doc_id,
                "text": f"Sparse doc {doc_id}",
                "metadata": {"source": "fake"},
                "bm25_score": random.random()
            })
        all_dense.append(query_dense)
        all_sparse.append(query_sparse)

    dense_rrf = reciprocal_rank_fusion(all_dense)
    sparse_rrf = reciprocal_rank_fusion(all_sparse)

    # ------------------ ORIGINAL CODE ------------------
    start_time_original = time.time()

    # RUN THIS 10 TIMES TO AMPLIFY THE TIME
    for _ in range(10):
        dense_original = []
        for cid, score in dense_rrf.items():
            for d_list in all_dense:
                for d in d_list:
                    if d["id"] == cid:
                        d_copy = d.copy()
                        d_copy["semantic_score"] = score
                        dense_original.append(d_copy)
                        break
                else:
                    continue
                break

        sparse_original = []
        for cid, score in sparse_rrf.items():
            for s_list in all_sparse:
                for s in s_list:
                    if s["id"] == cid:
                        s_copy = s.copy()
                        s_copy["bm25_score"] = score
                        sparse_original.append(s_copy)
                        break
                else:
                    continue
                break

    end_time_original = time.time()
    duration_original = end_time_original - start_time_original

    print(f"Original Time: {duration_original:.6f} seconds")

    # ------------------ OPTIMIZED CODE ------------------
    start_time_optimized = time.time()

    for _ in range(10):
        # Create mapping before loop
        dense_map = {}
        for d_list in all_dense:
            for d in d_list:
                if d["id"] not in dense_map:
                    dense_map[d["id"]] = d

        dense_optimized = []
        for cid, score in dense_rrf.items():
            if cid in dense_map:
                d_copy = dense_map[cid].copy()
                d_copy["semantic_score"] = score
                dense_optimized.append(d_copy)

        sparse_map = {}
        for s_list in all_sparse:
            for s in s_list:
                if s["id"] not in sparse_map:
                    sparse_map[s["id"]] = s

        sparse_optimized = []
        for cid, score in sparse_rrf.items():
            if cid in sparse_map:
                s_copy = sparse_map[cid].copy()
                s_copy["bm25_score"] = score
                sparse_optimized.append(s_copy)

    end_time_optimized = time.time()
    duration_optimized = end_time_optimized - start_time_optimized

    print(f"Optimized Time: {duration_optimized:.6f} seconds")
    print(f"Speedup: {duration_original / duration_optimized:.2f}x")

if __name__ == "__main__":
    run_benchmark()
