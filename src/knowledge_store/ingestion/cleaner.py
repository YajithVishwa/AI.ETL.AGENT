import re
from typing import List
from langchain_core.documents import Document


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def clean_documents(documents: List[Document]) -> List[Document]:
    cleaned_documents = []
    for document in documents:
        text = clean_text(document.page_content)
        if not text:
            continue
        cleaned_documents.append(
            Document(
                page_content=text,
                metadata=document.metadata,
            )
        )
    return cleaned_documents