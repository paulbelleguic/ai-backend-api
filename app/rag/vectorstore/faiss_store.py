from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


from app.rag.config import settings


class VectorStoreManager:
    """Gere la creation, la sauvegarde et le chargement de l'index FAISS."""

    def __init__(self) -> None:
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def create_vectorstore(self, documents: List[Document]) -> FAISS:
        if not documents:
            raise ValueError("La liste de documents est vide.")

        return FAISS.from_documents(documents, self.embeddings)

    def save_vectorstore(self, vectorstore: FAISS) -> None:
        output_path = Path(settings.VECTORSTORE_PATH)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        vectorstore.save_local(str(output_path))

    def load_vectorstore(self) -> FAISS:
        input_path = Path(settings.VECTORSTORE_PATH)

        if not input_path.exists():
            raise FileNotFoundError(
                f"Index FAISS introuvable : {settings.VECTORSTORE_PATH}"
            )

        return FAISS.load_local(
            str(input_path),
            self.embeddings,
            allow_dangerous_deserialization=True
        )
