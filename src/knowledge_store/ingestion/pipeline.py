from typing import List
from .loader import load_document
from .cleaner import clean_documents
from .splitter import split_documents
from uuid import uuid4
from ..vectorstore import ChromaVectorStore
from ..embeddings import get_embedding_model
import os

def ingest_file(file_path: str):

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'{file_path} not valid path')

    # 1. Load
    documents = load_document(file_path)

    # 2. Clean
    documents = clean_documents(documents)

    # 3. Split
    chunks = split_documents(documents)

    # 4. Initialize embedding model
    embedding_model = get_embedding_model()

    # 5. Initialize ChromaDB
    vector_store = ChromaVectorStore(
        collection_name="documents"
    )

    # 6. Embed and store each chunk
    for index, chunk in enumerate(chunks):

        vector = embedding_model.embed_query(
            chunk.page_content
        )

        vector_store.add_vector(
            vector_id=str(uuid4()),
            vector=vector,
            metadata={
                **chunk.metadata,
                "chunk_index": index,
                "source": file_path,
            },
            document=chunk.page_content,
        )