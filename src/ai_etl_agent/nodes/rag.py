from ..state import AgentState
from typing import Any, Dict
from ...knowledge_store import ChromaVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

class RagNode:
    def __init__(self, vector_store: ChromaVectorStore, embedding_model: HuggingFaceEmbeddings):
        self.vector_store = vector_store
        self.embedding_model = embedding_model

    def __call__(self, state: AgentState) -> Dict[str, Any]:
        query = state["user_query"]
        query_embedding = self.embedding_model.embed_query(query)
        results = self.vector_store.query_vector(
            vector=query_embedding,
            top_k=5,
        )
        return {
            "rag_query": query,
            "rag_results": results,
            "current_step": "rag_completed",
        }