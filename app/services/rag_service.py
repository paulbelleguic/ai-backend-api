from typing import Any

from app.schemas.chat import ChatRequest, ChatResponse


class RAGService:
    def __init__(self):
        self.pipeline: Any | None = None

    def _get_pipeline(self) -> Any:
        if self.pipeline is None:
            from app.rag.assistant.pipeline import EcommerceAssistantPipeline

            self.pipeline = EcommerceAssistantPipeline()

        return self.pipeline

    def answer(self, data: ChatRequest) -> ChatResponse:
        history = None

        if data.history:
            history = [message.model_dump() for message in data.history]

        result = self._get_pipeline().ask(
            query=data.question,
            history=history,
        )

        return ChatResponse(
            answer=result["answer"],
            route=result["route"],
            sources=result["sources"],
        )


rag_service = RAGService()
