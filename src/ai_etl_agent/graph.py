from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from ai_etl_agent.nodes import analyzer_node, planner_node, RagNode, tool_node, agent_node
from ai_etl_agent.state import AgentState
from functools import partial

def route_after_planner(state: AgentState):
    """
        Decide which node should execute after planning.
    """

    needs_rag = state.get(
        "needs_rag",
        False,
    )

    needs_tools = state.get(
        "needs_tools",
        False,
    )

    if needs_rag:
        return "rag"

    if needs_tools:
        return "agent"

    return "analyzer"

def route_after_agent(state: AgentState):

    messages = state.get("messages", [])

    if not messages:
        return "end"

    last_message = messages[-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return "end"

def build_graph(llm, mcp_tools, vector_store, embedding_model) -> CompiledStateGraph:
    rag_node = RagNode(vector_store=vector_store, embedding_model=embedding_model)
    builder = StateGraph(AgentState)
    builder.add_node('planner', planner_node)
    builder.add_node('tools', partial(tool_node, tools=mcp_tools))
    builder.add_node('rag', rag_node)
    builder.add_node('analyzer', partial(analyzer_node, llm=llm))
    builder.add_node('agent', partial(agent_node, llm=llm, mcp_tools=mcp_tools))

    builder.add_edge(START, 'planner')
    builder.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "rag": "rag",
            "agent": "agent",
            "analyzer": "analyzer",
        },
    )
    builder.add_edge("rag", "analyzer")
    builder.add_conditional_edges(
        "agent",
        route_after_agent,
        {
            "tools": "tools",
            "end": END,
        },
    )
    builder.add_edge('tools', 'agent')
    builder.add_edge('analyzer', END)

    return builder.compile()