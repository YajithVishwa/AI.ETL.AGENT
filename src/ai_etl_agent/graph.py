from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from .nodes import analyzer_node, planner_node, RagNode, tool_node
from .state import AgentState

def route_after_planner(state: AgentState):
    """
        Decide whether the graph should execute RAG,
        MCP tools, or go directly to analysis.
    """

    if state.get("needs_rag", False):
        return "rag"

    if state.get("needs_tools", False):
        return "tools"

    return "analyzer"

def build_graph(llm, vector_store, embedding_model) -> CompiledStateGraph:
    rag_node = RagNode(vector_store=vector_store, embedding_model=embedding_model)
    builder = StateGraph(AgentState)
    builder.add_node('planner', planner_node)
    builder.add_node('tools', tool_node)
    builder.add_node('rag', rag_node)
    builder.add_node('analyzer', lambda state: analyzer_node(state, llm))

    builder.add_edge(START, 'planner')
    builder.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "rag": "rag",
            "tools": "tools",
            "analyzer": "analyzer",
        },
    )
    builder.add_edge("rag", "analyzer")
    builder.add_edge('tools', 'analyzer')
    builder.add_edge('analyzer', END)

    return builder.compile()