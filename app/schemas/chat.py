from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., example="user")
    content: str = Field(..., example="Je cherche un produit pas cher")
    route: str | None = Field(default=None, example="catalog")


class ChatRequest(BaseModel):
    question: str = Field(..., example="Quels produits me recommandes-tu ?")
    history: list[ChatMessage] | None = None


class ChatResponse(BaseModel):
    answer: str
    route: str
    sources: list[str]
