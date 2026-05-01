import unicodedata
from typing import Any

from app.rag.catalog.pipeline import CatalogPipeline
from app.rag.routing.classifier import QueryRouter


class EcommerceAssistantPipeline:
    """Pipeline hybride qui route une question vers la FAQ ou le catalogue."""

    def __init__(self) -> None:
        self.router = QueryRouter()
        self.support_pipeline: Any | None = None
        self.catalog_pipeline: CatalogPipeline | None = None

    def _get_support_pipeline(self) -> Any:
        if self.support_pipeline is None:
            from app.rag.pipeline import RAGPipeline

            self.support_pipeline = RAGPipeline()
        return self.support_pipeline

    def _get_catalog_pipeline(self) -> CatalogPipeline:
        if self.catalog_pipeline is None:
            self.catalog_pipeline = CatalogPipeline()
        return self.catalog_pipeline

    def ask(self, query: str, history: list[dict] | None = None) -> dict:
        if not query.strip():
            raise ValueError("La question utilisateur ne peut pas etre vide.")

        follow_up = self._is_follow_up(query)
        preferred_route = self._get_last_assistant_route(history) if follow_up else None
        effective_query = self._build_effective_query(
            query=query,
            history=history,
            preferred_route=preferred_route,
        )
        routing = self.router.route(effective_query)

        if preferred_route in {"support", "catalog"}:
            routing["route"] = preferred_route

        if routing["route"] == "catalog":
            catalog_result = self._get_catalog_pipeline().search_from_query(effective_query)
            answer = self._build_catalog_answer(catalog_result["formatted_results"])

            return {
                "query": query,
                "effective_query": effective_query,
                "route": "catalog",
                "answer": answer,
                "sources": ["data/raw/products.csv"],
                "details": {
                    "filters": catalog_result["filters"],
                    "count": catalog_result["count"],
                    "formatted_results": catalog_result["formatted_results"],
                },
                "routing": routing,
            }

        support_result = self._get_support_pipeline().ask(question=effective_query, k=4)

        return {
            "query": query,
            "effective_query": effective_query,
            "route": "support",
            "answer": support_result["answer"],
            "sources": support_result["sources"],
            "details": {
                "passages": support_result["passages"],
                "context": support_result["context"],
            },
            "routing": routing,
        }

    @staticmethod
    def _build_catalog_answer(formatted_results: str) -> str:
        if formatted_results == "Aucun produit correspondant n'a ete trouve.":
            return formatted_results

        return "J'ai trouve les produits suivants :\n" + formatted_results

    def _build_effective_query(
        self,
        query: str,
        history: list[dict] | None = None,
        preferred_route: str | None = None,
    ) -> str:
        if not history:
            return query

        normalized_query = self._normalize_text(query)
        follow_up_starts = ("et ", "sinon", "avec ", "sans ", "en ", "pour ", "plutot")

        if len(normalized_query.split()) > 4 and not normalized_query.startswith(follow_up_starts):
            return query

        last_user_query = self._get_last_user_query(history)
        if not last_user_query:
            return query

        if preferred_route == "catalog":
            return f"{query} ; produit precedent : {last_user_query}"

        return f"{last_user_query} ; suivi client : {query}"

    @staticmethod
    def _get_last_user_query(history: list[dict]) -> str | None:
        for message in reversed(history):
            if message.get("role") == "user":
                return message.get("content")
        return None

    @staticmethod
    def _get_last_assistant_route(history: list[dict] | None) -> str | None:
        if not history:
            return None

        for message in reversed(history):
            if message.get("role") == "assistant":
                return message.get("route")
        return None

    def _is_follow_up(self, query: str) -> bool:
        normalized_query = self._normalize_text(query)
        follow_up_starts = ("et ", "sinon", "avec ", "sans ", "en ", "pour ", "plutot")
        return len(normalized_query.split()) <= 4 or normalized_query.startswith(follow_up_starts)

    @staticmethod
    def _normalize_text(text: str) -> str:
        text = text.lower()
        text = unicodedata.normalize("NFKD", text)
        return "".join(char for char in text if not unicodedata.combining(char))
