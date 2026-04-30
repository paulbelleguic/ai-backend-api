from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


class DocumentLoader:
    """Charge des documents texte ou PDF et les convertit en objets Document."""

    SUPPORTED_EXTENSIONS = {".pdf", ".txt"}

    def load_documents(self, file_path: str) -> List[Document]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {file_path}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Format non supporté : {path.suffix}. "
                f"Formats acceptés : {self.SUPPORTED_EXTENSIONS}"
            )

        if path.suffix.lower() == ".pdf":
            loader = PyPDFLoader(str(path))
        else:
            loader = TextLoader(str(path), encoding="utf-8")

        documents = loader.load()

        if not documents:
            raise ValueError("Aucun contenu n'a été chargé depuis le document.")

        return documents

