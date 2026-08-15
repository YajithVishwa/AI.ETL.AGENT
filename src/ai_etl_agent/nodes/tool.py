from langgraph.prebuilt import ToolNode
from langchain_core.messages import ToolMessage
from ai_etl_agent.state import AgentState
from ai_etl_agent.utils import logger

async def tool_node(state: AgentState, tools) -> AgentState:
    """Execute tools from the agent state and return updated state with results."""
    try:
        node = ToolNode(tools=tools)
        result = await node.ainvoke(state)
        return {**state, **result} if isinstance(result, dict) else state
    except Exception as e:
        logger.error(f"Tool execution error: {e}", exc_info=True)
        last_message = state["messages"][-1]
        tool_calls = getattr(last_message, "tool_calls", None) or []
        error_messages = [
            ToolMessage(
                content=f"Tool execution failed: {str(e)}",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
        return {
            **state,
            "messages": state["messages"] + error_messages,
            "tool_results": None,
            "error": f"Tool execution failed: {str(e)}",
            "current_step": "tool_execution_failed",
        }