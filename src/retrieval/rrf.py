def reciprocal_rank_fusion(
    results_lists: list[list[dict]],
    k: int = 60
) -> dict[str, float]:
    """Applies Reciprocal Rank Fusion to multiple lists of retrieved items.

    Args:
        results_lists: A list of result lists. Each result list contains dictionaries
                       with at least an "id" key.
        k: The constant used in the RRF formula (default is 60).

    Returns:
        A dictionary mapping item IDs to their fused RRF score.
    """
    fused_scores: dict[str, float] = {}

    for results in results_lists:
        for rank, result in enumerate(results, start=1):
            item_id = result["id"]
            if item_id not in fused_scores:
                fused_scores[item_id] = 0.0

            fused_scores[item_id] += 1.0 / (k + rank)

    return fused_scores
