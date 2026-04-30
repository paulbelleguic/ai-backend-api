from fastapi import APIRouter

from app.schemas.predict import PredictRequest, PredictResponse
from app.services.ml_service import ml_service

router = APIRouter()


@router.post("/", response_model=PredictResponse)
def predict(payload: PredictRequest):
    return ml_service.predict(payload)
