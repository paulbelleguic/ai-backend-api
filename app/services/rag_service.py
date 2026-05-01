import re
import unicodedata
from pathlib import Path

from app.rag.catalog.pipeline import CatalogPipeline
from app.rag.routing.classifier import QueryRouter
from app.schemas.chat import ChatRequest, ChatResponse


class RAGService:
    """Lightweight production chat service for the deployed API.

    The original local project can use FAISS and a local Transformers model, but
    Render free instances are too small for that path to be reliable. This
    service keeps the same API contract and routes to either catalog search or a
    simple FAQ extractive answer without loading the heavy RAG stack.
    """

    def __init__(self):
        self.router = QueryRouter()
        self.catalog_pipeline: CatalogPipeline | None = None
        self.faq_text: str | None = None

    def _get_catalog_pipeline(self) -> CatalogPipeline:
        if self.catalog_pipeline is None:
            self.catalog_pipeline = CatalogPipeline()
        return self.catalog_pipeline

    def _get_faq_text(self) -> str:
        if self.faq_text is None:
            self.faq_text = Path("data/raw/faq.txt").read_text(encoding="utf-8")
        return self.faq_text

    def answer(self, data: ChatRequest) -> ChatResponse:
        question = data.question.strip()
        routing = self.router.route(question)

        if routing["route"] == "catalog":
            catalog_result = self._get_catalog_pipeline().search_from_query(question)
            formatted_results = catalog_result["formatted_results"]
            answer = self._build_catalog_answer(formatted_results)

            return ChatResponse(
                answer=answer,
                route="catalog",
                sources=["data/raw/products.csv"],
            )

        return ChatResponse(
            answer=self._answer_from_faq(question),
            route="support",
            sources=["data/raw/faq.txt"],
        )

    @staticmethod
    def _build_catalog_answer(formatted_results: str) -> str:
        if formatted_results == "Aucun produit correspondant n'a ete trouve.":
            return formatted_results

        return "J'ai trouve les produits suivants :\n" + formatted_results

    def _answer_from_faq(self, question: str) -> str:
        faq_text = self._get_faq_text()
        sections = self._split_faq_sections(faq_text)
        keywords = self._extract_keywords(question)

        if not sections:
            return "Je ne dispose pas de contexte suffisant pour repondre."

        if not keywords:
            title, content = sections[0]
        else:
            title, content = max(
                sections,
                key=lambda section: self._score_section(section, keywords),
            )

        sentences = self._extract_sentences(content)
        selected = sentences[:3] if sentences else [content.strip()]

        return f"Selon notre FAQ ({title}), " + " ".join(selected)

    @staticmethod
    def _split_faq_sections(text: str) -> list[tuple[str, str]]:
        blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
        sections = []

        for index in range(0, len(blocks), 2):
            title = blocks[index].strip()
            content = blocks[index + 1].strip() if index + 1 < len(blocks) else ""
            if content:
                sections.append((title, content))

        return sections

    @staticmethod
    def _extract_sentences(text: str) -> list[str]:
        return [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+", text.replace("\n", " "))
            if sentence.strip()
        ]

    @staticmethod
    def _score_section(section: tuple[str, str], keywords: list[str]) -> int:
        title, content = section
        normalized = RAGService._normalize_text(f"{title} {content}")
        return sum(1 for keyword in keywords if keyword in normalized)

    @staticmethod
    def _extract_keywords(text: str) -> list[str]:
        normalized = RAGService._normalize_text(text)
        tokens = re.findall(r"\b\w+\b", normalized)
        stopwords = {
            "qu", "que", "quoi", "qui", "de", "du", "des", "le", "la", "les",
            "un", "une", "est", "et", "a", "au", "aux", "en", "dans", "sur",
            "pour", "par", "comment", "pourquoi", "ce", "cette", "ces", "mon",
            "ma", "mes", "vos", "votre", "je", "tu", "il", "elle", "nous",
            "vous", "ils", "elles", "avec",
        }
        return [token for token in tokens if token not in stopwords and len(token) > 2]

    @staticmethod
    def _normalize_text(text: str) -> str:
        text = text.lower()
        text = unicodedata.normalize("NFKD", text)
        return "".join(char for char in text if not unicodedata.combining(char))


rag_service = RAGService()
