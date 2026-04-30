from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import rag_service

router = APIRouter()


@router.post("/", response_model=ChatResponse)
def chat(payload: ChatRequest):
    return rag_service.answer(payload)
