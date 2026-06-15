from src.agent.state import AgentState
from src.generation.confidence import score_confidence

def reason_step(state: AgentState) -> AgentState:
    """The Reasoning Agent decides if we have enough information to answer."""
    chunks = state.get("retrieved_chunks", [])
    query = state["query"]

    # Assess confidence using the pipeline's lexical/semantic overlap approach
    confidence = score_confidence(query, chunks)

    # Determine if we have sufficient coverage, or if we hit the attempt limit
    is_sufficient = confidence["label"] in ("high", "medium")
    max_attempts_reached = state.get("attempts", 1) >= 3

    reasoning = [f"Confidence: {confidence['label']} ({confidence['score']:.2f})"]
    if is_sufficient:
        reasoning.append("Sufficient information retrieved.")
    elif max_attempts_reached:
        reasoning.append("Max retrieval attempts reached.")
    else:
        reasoning.append("Insufficient information. Needs retry.")

    return {
        **state,
        "confidence": confidence,
        "sufficient": is_sufficient or max_attempts_reached,
        "reasoning": state.get("reasoning", []) + reasoning
    }
