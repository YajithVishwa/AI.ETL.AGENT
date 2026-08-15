from typing import TypedDict, List, Any
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: List[BaseMessage]
    user_query: str
    plan: List[str]
    current_step: str
    rag_query: str
    rag_results: List[Any]
    tool_results: List[Any]
    analysis: str
    final_response: str
    needs_rag: bool
    needs_tools: bool
    requires_approval: bool
