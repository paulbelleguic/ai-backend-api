from fastapi import FastAPI

from app.api.routes.predict import router as predict_router
from app.api.routes.chat import router as chat_router

app = FastAPI(
    title="AI Backend API",
    description="API FastAPI pour servir un modèle ML et un chatbot RAG.",
    version="0.1.0",
)

app.include_router(predict_router, prefix="/predict", tags=["Prediction"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])


@app.get("/")
def root():
    return {
        "message": "AI Backend API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
