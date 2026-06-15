import math

def precision_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
    retrieved_k = retrieved_ids[:k]
    if not retrieved_k:
        return 0.0
    relevant_retrieved = sum(1 for doc_id in retrieved_k if doc_id in relevant_ids)
    return relevant_retrieved / len(retrieved_k)

def recall_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
    if not relevant_ids:
        return 1.0
    retrieved_k = retrieved_ids[:k]
    relevant_retrieved = sum(1 for doc_id in retrieved_k if doc_id in relevant_ids)
    return relevant_retrieved / len(relevant_ids)

def mrr_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
    for rank, doc_id in enumerate(retrieved_ids[:k], start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0

def ndcg_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
    dcg = 0.0
    for rank, doc_id in enumerate(retrieved_ids[:k], start=1):
        if doc_id in relevant_ids:
            dcg += 1.0 / math.log2(rank + 1)

    idcg = 0.0
    for rank in range(1, min(len(relevant_ids), k) + 1):
        idcg += 1.0 / math.log2(rank + 1)

    if idcg == 0.0:
        return 0.0
    return dcg / idcg

def calculate_groundedness(answer: str, retrieved_chunks: list[dict]) -> float:
    """A minimal heuristic: grounded if it contains citation markers mapped to chunks."""
    if not answer or not retrieved_chunks:
        return 0.0
    # Check for citation markers like [1], [2], etc.
    markers = [f"[{i}]" for i in range(1, len(retrieved_chunks) + 1)]
    found = sum(1 for m in markers if m in answer)
    return found / len(retrieved_chunks) if retrieved_chunks else 0.0
