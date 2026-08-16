from typing import TypedDict, List, Any, Annotated, Dict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_query: str
    plan: List[str]
    current_step: str
    rag_query: str
    rag_results: List[Any]
    tool_results: List[Any]
    references: List[Dict[str, Any]]
    analysis: str
    final_response: str
    needs_rag: bool
    needs_tools: bool
    requires_approval: bool
