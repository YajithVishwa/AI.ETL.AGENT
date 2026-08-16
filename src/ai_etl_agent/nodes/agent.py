from ai_etl_agent.state import AgentState

def agent_node(state: AgentState, llm, mcp_tools) -> AgentState:
    llm_with_tools = llm.bind_tools(mcp_tools)
    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        **state,
        "messages": state["messages"] + [response],
        "final_response": response.content,
    }