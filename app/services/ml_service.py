from pathlib import Path

import joblib
import pandas as pd

from app.schemas.predict import PredictRequest, PredictResponse


class MLService:
    def __init__(self):
        model_path = Path("app/models/baseline_sales_model.joblib")

        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")

        self.model = joblib.load(model_path)

    def predict(self, data: PredictRequest) -> PredictResponse:
        input_data = pd.DataFrame([data.model_dump()])

        prediction = self.model.predict(input_data)[0]

        return PredictResponse(
            prediction=float(prediction)
        )


ml_service = MLService()

