from src.agent.state import AgentState
from src.generation.citation import build_citations


class ResponseAgent:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def respond_step(self, state: AgentState) -> AgentState:
        """The Response Agent synthesis the final answer and citations."""
        query = state["query"]
        chunks = state["retrieved_chunks"]
        confidence = state["confidence"]

        answer = self.pipeline.generator.generate(query, chunks, confidence)
        citations = build_citations(chunks)

        return {
            **state,
            "answer": answer,
            "citations": citations
        }
