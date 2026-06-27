from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from src.agent.planner import plan_step
from src.agent.reasoner import reason_step
from src.agent.responder import ResponseAgent
from src.agent.retriever import RetrievalAgent
from src.agent.state import AgentState


class AgenticRAG:
    """Agentic RAG orchestrator using LangGraph."""

    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.retrieval_agent = RetrievalAgent(pipeline)
        self.response_agent = ResponseAgent(pipeline)

        self.graph = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        # Nodes
        workflow.add_node("plan", plan_step)
        workflow.add_node("retrieve", self.retrieval_agent.retrieve_step)
        workflow.add_node("reason", reason_step)
        workflow.add_node("respond", self.response_agent.respond_step)

        # Edges
        workflow.set_entry_point("plan")
        workflow.add_edge("plan", "retrieve")
        workflow.add_edge("retrieve", "reason")

        # Conditional Edge
        def route_after_reasoning(state: AgentState):
            if state.get("sufficient"):
                return "respond"
            return "plan"

        workflow.add_conditional_edges(
            "reason",
            route_after_reasoning,
            {"respond": "respond", "plan": "plan"}
        )

        workflow.add_edge("respond", END)

        # Compile with in-memory state persistence
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)

    def query(self, query: str, role: str = None, user_id: str = "", thread_id: str = "default"):
        """Run a query through the agentic graph."""
        initial_state = AgentState(
            query=query,
            role=role,
            user_id=user_id,
            sub_queries=[],
            retrieved_chunks=[],
            reasoning=[],
            attempts=0,
            sufficient=False,
            answer="",
            confidence={},
            citations=[]
        )

        config = {"configurable": {"thread_id": thread_id}}
        final_state = self.graph.invoke(initial_state, config=config)

        return final_state
