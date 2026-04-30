from typing import List

from langchain_core.documents import Document

from app.rag.vectorstore.faiss_store import VectorStoreManager


class Retriever:
    """Interroge l'index FAISS pour retrouver les documents les plus pertinents."""

    def __init__(self) -> None:
        self.vectorstore_manager = VectorStoreManager()
        self.vectorstore = self.vectorstore_manager.load_vectorstore()

    def retrieve(self, query: str, k: int = 3) -> List[Document]:
        return [item["document"] for item in self.retrieve_with_scores(query=query, k=k)]

    def retrieve_with_scores(self, query: str, k: int = 3) -> List[dict]:
        if not query.strip():
            raise ValueError("La question utilisateur ne peut pas etre vide.")

        if k <= 0:
            raise ValueError("k doit etre strictement superieur a 0.")

        results = self.vectorstore.similarity_search_with_score(query, k=k)

        return [
            {"document": document, "score": float(score)}
            for document, score in results
        ]
