from src.agent.state import AgentState

def plan_step(state: AgentState) -> AgentState:
    """The Planner Agent parses the initial query to decompose it or set up execution steps."""
    query = state["query"]

    # Simple rule-based planner for offline default
    # In a full deployment, this could call an LLM to decompose complex queries
    sub_queries = [query]

    if " and " in query.lower():
        parts = query.lower().split(" and ")
        sub_queries = parts

    return {
        **state,
        "sub_queries": sub_queries,
        "attempts": state.get("attempts", 0) + 1
    }
