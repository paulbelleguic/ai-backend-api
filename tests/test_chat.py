from fastapi.testclient import TestClient

from app.main import app
from app.schemas.chat import ChatResponse
from app.services.rag_service import rag_service


def test_chat_returns_answer(monkeypatch):
    def fake_answer(payload):
        return ChatResponse(
            answer="J'ai trouve les produits suivants : exemple",
            route="catalog",
            sources=["data/raw/products.csv"],
        )

    monkeypatch.setattr(rag_service, "answer", fake_answer)
    client = TestClient(app)

    response = client.post(
        "/chat/",
        json={
            "question": "je cherche des produits pas chers",
            "history": [],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "J'ai trouve les produits suivants : exemple",
        "route": "catalog",
        "sources": ["data/raw/products.csv"],
    }


def test_chat_validates_required_question():
    client = TestClient(app)

    response = client.post("/chat/", json={"history": []})

    assert response.status_code == 422
