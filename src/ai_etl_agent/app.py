import os
import asyncio
from unittest import result
import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

import logging
for noisy in ("httpx", "httpcore", "urllib3", "huggingface_hub"):
    logging.getLogger(noisy).setLevel(logging.WARNING)

logging.getLogger("transformers").setLevel(logging.ERROR)

from knowledge_store import get_embedding_model, ChromaVectorStore
from ai_etl_agent.graph import build_graph
from ai_etl_agent.mcp_client import MCPClient


# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------

load_dotenv(
    os.path.normpath(
        os.path.join(os.path.abspath(__file__), "../../../.env")
    )
)


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI ETL Agent",
    page_icon="🤖",
    layout="wide",
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


if "graph" not in st.session_state:
    st.session_state.graph = None


# ---------------------------------------------------------
# Initialize Agent
# ---------------------------------------------------------

async def initialize_graph():

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

    mcp_client = MCPClient()

    mcp_tools = await mcp_client.get_tools()

    vector_store = ChromaVectorStore(
        collection_name="ai_etl_agent"
    )

    embedding_model = get_embedding_model()

    graph = build_graph(
        llm=llm,
        mcp_tools=mcp_tools,
        vector_store=vector_store,
        embedding_model=embedding_model,
    )

    return graph


# ---------------------------------------------------------
# Async helper
# ---------------------------------------------------------

async def get_graph():

    if st.session_state.graph is None:
        st.session_state.graph = await initialize_graph()

    return st.session_state.graph


async def invoke_agent(user_query: str):

    graph = await get_graph()

    result = await graph.ainvoke(
        {
            "user_query": user_query,
            "messages": [
                HumanMessage(content=user_query)
            ],
        },
        config={
            "recursion_limit": 5,
        },
    )

    return result


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.title("⚙️ AI ETL Agent")

    st.markdown(
        """
        **Capabilities**

        - 🔎 RAG / Knowledge Search
        - 🔧 MCP Tools
        - 🧠 LangGraph
        - 🗄️ ChromaDB
        - 🤖 Groq LLM
        """
    )

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


# ---------------------------------------------------------
# Main UI
# ---------------------------------------------------------

st.title("🤖 AI ETL Agent")

st.caption(
    "LangGraph + MCP + RAG + ChromaDB + Groq"
)


# ---------------------------------------------------------
# Display previous messages
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------

user_query = st.chat_input(
    "Ask your ETL agent something..."
)


if user_query:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_query)


    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                result = asyncio.run(
                    invoke_agent(user_query)
                )
                response = result["final_response"]
                references = result.get("references", [])

                st.markdown(response)

                if references:
                    with st.expander("📚 References"):
                        for i, reference in enumerate(references, start=1):
                            filename = reference.get(
                                "filename",
                                "Unknown source"
                            )
                            page = reference.get("page")
                            chunk = reference.get("chunk_index")
                            reference_text = f"**{i}. {filename}**"
                            if page is not None:
                                reference_text += f" — Page {page}"
                            if chunk is not None:
                                reference_text += f" — Chunk {chunk}"
                            st.markdown(reference_text)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )

            except Exception as e:

                error_message = f"❌ Error: {str(e)}"

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message,
                    }
                )