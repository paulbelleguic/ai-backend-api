from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., json_schema_extra={"example": "user"})
    content: str = Field(..., json_schema_extra={"example": "Je cherche un produit pas cher"})
    route: str | None = Field(default=None, json_schema_extra={"example": "catalog"})


class ChatRequest(BaseModel):
    question: str = Field(..., json_schema_extra={"example": "Quels produits me recommandes-tu ?"})
    history: list[ChatMessage] | None = None


class ChatResponse(BaseModel):
    answer: str
    route: str
    sources: list[str]
