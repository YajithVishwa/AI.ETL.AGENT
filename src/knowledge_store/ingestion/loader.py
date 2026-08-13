import os 
from langchain_core.documents import Document
from typing import List
from langchain_pymupdf4llm import PyMuPDF4LLMLoader

SUPPORTED_EXTENSION = {
    '.pdf'
}

def load_document(file_path: str) -> List[Document]:
    file_name, file_extension = os.path.splitext(file_path)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = file_extension.lower()

    if extension == ".pdf":
        loader = PyMuPDF4LLMLoader(str(file_path))
        return loader.load()

    raise ValueError(
        f"Unsupported file type: {extension}. Supported types: {SUPPORTED_EXTENSION}"
    )