from langchain_core.tools import ToolNode
from ..state import AgentState
from ..utils import logger

def tool_node(state: AgentState, tools) -> AgentState:
    """Execute tools from the agent state and return updated state with results."""
    try:
        node = ToolNode(tools=tools)
        result = node.invoke(state)
        return {**state, **result} if isinstance(result, dict) else state
    except Exception as e:
        logger.error(f"Tool execution error: {e}", exc_info=True)
        return {
            **state,
            "tool_results": None,
            "error": f"Tool execution failed: {str(e)}",
            "current_step": "tool_execution_failed"
        }