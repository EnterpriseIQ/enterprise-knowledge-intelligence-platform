from src.agent.state import AgentState
from src.retrieval.cross_source import diversify


class RetrievalAgent:
    def __init__(self, pipeline):
        """Initialise with a reference to the main RAGPipeline to re-use routing/hybrid ret."""
        self.pipeline = pipeline

    def retrieve_step(self, state: AgentState) -> AgentState:
        """The Retrieval Agent runs retrieval for all sub-queries and aggregates them."""
        all_chunks = []

        # Execute retrieval for each planned sub-query
        for sq in state["sub_queries"]:
            route = self.pipeline.router.classify(sq)

            chunks, _ = self.pipeline.retriever.retrieve(
                sq, role=state["role"], route=route, user_id=state["user_id"]
            )
            all_chunks.extend(chunks)

        # Diversify to prevent one sub-query from dominating
        diversified_chunks = diversify(all_chunks, top_k=10)

        return {**state, "retrieved_chunks": diversified_chunks}
