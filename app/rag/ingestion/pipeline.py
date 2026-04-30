from pathlib import Path

from app.rag.ingestion.loader import DocumentLoader
from app.rag.ingestion.splitter import DocumentSplitter
from app.rag.vectorstore.faiss_store import VectorStoreManager


class IngestionPipeline:
    """Orchestre l'ingestion d'un document et la reconstruction de l'index."""

    def __init__(
        self,
        chunk_size: int = 150,
        chunk_overlap: int = 30,
    ) -> None:
        self.loader = DocumentLoader()
        self.splitter = DocumentSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        self.vectorstore_manager = VectorStoreManager()

    def ingest_file(self, file_path: str) -> int:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {file_path}")

        documents = self.loader.load_documents(str(path))
        chunks = self.splitter.split_documents(documents)
        vectorstore = self.vectorstore_manager.create_vectorstore(chunks)
        self.vectorstore_manager.save_vectorstore(vectorstore)

        return len(chunks)
