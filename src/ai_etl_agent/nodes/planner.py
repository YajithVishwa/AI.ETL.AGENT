from langchain_core.messages import HumanMessage
from ..state import AgentState

def planner_node(state: AgentState) -> AgentState:
    """
        Creates an investigation plan based on the user's prompt.
    """
    user_query = state['user_query'].lower()
    plan = [
        "Understand the user request",
        "Determine whether organizational knowledge is required",
        "Determine whether external system tools are required",
        "Analyze the gathered information",
        "Generate final response",
    ]

    needs_rag = any(keyword in user_query for keyword in ['why', 'how', 'documentation', 'architecture', 'guideline'])

    needs_tools = any(keyword in user_query for keyword in ['run', 'check', 'job', 'pipeline', 'execute', 'query', 'table'])

    return {
        "plan": plan,
        "needs_rag": needs_rag,
        "needs_tools": needs_tools,
        "current_step": "planning_completed"
    }