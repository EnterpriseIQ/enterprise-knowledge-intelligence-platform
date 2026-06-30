from typing import TypedDict

from src.security.rbac import AccessDecision


class AgentState(TypedDict):
    """The state of the agent workflow."""

    query: str
    role: str | None
    user_id: str

    # Accumulated intermediate state
    sub_queries: list[str]
    retrieved_chunks: list[dict]
    access_decisions: list[AccessDecision]
    reasoning: list[str]

    # Routing control
    attempts: int
    sufficient: bool

    # Final outputs
    answer: str
    confidence: dict
    citations: list
