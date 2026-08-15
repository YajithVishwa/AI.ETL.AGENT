from langchain_core.messages import HumanMessage, SystemMessage
from ..state import AgentState


def analyzer_node( state: AgentState, llm) -> AgentState:

    user_query = state["user_query"]

    rag_results = state.get("rag_results", [])
    tool_results = state.get("tool_results", [])

    context = f"""
        User Query:
        {user_query}

        RAG Results:
        {rag_results}

        MCP Tool Results:
        {tool_results}
    """

    system_prompt = SystemMessage(content="""
        You are a Data Engineering ETL AI Agent.
        Analyze the following information and answer the user's request. Also follow the rules.
        Rules:
        - Use the MCP results as live system information.
        - Use RAG results as organizational knowledge.
        - Do not invent system information.
        - Clearly explain the reasoning.
        - If the available information is insufficient, say so.
    """)

    response = llm.invoke( [system_prompt] + [ HumanMessage(content=context) ]  )

    return {
        "analysis": response.content,
        "final_response": response.content, # Add comment: "intentionally same for state tracking"
        "current_step": "analysis_completed",
    }