import os
import asyncio
import streamlit as st

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from knowledge_store import get_embedding_model, ChromaVectorStore, ingest_file


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

    uploaded_file = st.file_uploader(label="Upload PDF", type=["pdf"], key="file_uploader")
    if uploaded_file is not None:
        base_location = os.path.normpath(os.path.join(os.path.abspath(__file__), '../../knowledge_store/content'))
        if not os.path.exists(base_location):
            os.makedirs(base_location)
        file_path = os.path.join(base_location, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        ingest_file(file_path)


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

                st.markdown('Generating response...')

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": 'demo response',
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