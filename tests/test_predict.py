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
            "purchase_year": 2018,
            "purchase_month": 5,
            "purchase_day": 15,
            "purchase_hour": 12,
            "purchase_dayofweek": 2,
            "customer_state": "SP",
            "n_items": 2,
            "n_unique_products": 2,
            "n_unique_sellers": 1,
            "payment_installments_max": 3,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"prediction": 149.75}


def test_predict_validates_input():
    client = TestClient(app)

    response = client.post(
        "/predict/",
        json={
            "purchase_year": 2018,
            "purchase_month": 13,
            "purchase_day": 15,
            "purchase_hour": 12,
            "purchase_dayofweek": 2,
            "customer_state": "SP",
            "n_items": 2,
            "n_unique_products": 2,
            "n_unique_sellers": 1,
            "payment_installments_max": 3,
        },
    )

    assert response.status_code == 422
