from fastapi.testclient import TestClient

from app.main import app
from app.schemas.predict import PredictResponse
from app.services.ml_service import ml_service


def test_health_check():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_returns_prediction(monkeypatch):
    def fake_predict(payload):
        return PredictResponse(prediction=149.75)

    monkeypatch.setattr(ml_service, "predict", fake_predict)
    client = TestClient(app)

    response = client.post(
        "/predict/",
        json={
            "purchase_month": 5,
            "purchase_dayofweek": 2,
            "customer_state": "SP",
            "customer_city": "sao paulo",
            "payment_installments": 3,
            "items_count": 2,
            "freight_value": 21.5,
            "review_score": 4.0,
            "delivery_delay_days": 0,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"prediction": 149.75}


def test_predict_validates_input():
    client = TestClient(app)

    response = client.post(
        "/predict/",
        json={
            "purchase_month": 13,
            "purchase_dayofweek": 2,
            "customer_state": "SP",
            "customer_city": "sao paulo",
            "payment_installments": 3,
            "items_count": 2,
            "freight_value": 21.5,
            "review_score": 4.0,
            "delivery_delay_days": 0,
        },
    )

    assert response.status_code == 422
