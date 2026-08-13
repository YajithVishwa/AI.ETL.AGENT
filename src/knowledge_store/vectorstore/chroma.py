import chromadb
import os
from typing import List, Dict

class ChromaVectorStore:
    def __init__(self, collection_name: str):
        db_path = os.path.normpath(os.path.join(os.path.abspath(__file__), '../../db', 'chroma_db'))
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_vector(self, vector_id: str, vector: List, metadata: List[Dict] ):
        self.collection.add(
            ids=[vector_id],
            embeddings=[vector],
            metadatas=[metadata]
        )

    def query_vector(self, vector: List[float], top_k: int = 5):
        results = self.collection.query(
            query_embeddings=[vector],
            n_results=top_k
        )
        return results