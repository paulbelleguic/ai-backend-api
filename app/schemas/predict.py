from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    purchase_month: int = Field(..., ge=1, le=12, example=5)
    purchase_dayofweek: int = Field(..., ge=0, le=6, example=2)
    customer_state: str = Field(..., example="SP")
    customer_city: str = Field(..., example="sao paulo")
    payment_installments: int = Field(..., ge=1, example=3)
    items_count: int = Field(..., ge=1, example=2)
    freight_value: float = Field(..., ge=0, example=21.5)
    review_score: float = Field(..., ge=1, le=5, example=4.0)
    delivery_delay_days: int = Field(..., example=0)


class PredictResponse(BaseModel):
    prediction: float = Field(..., example=149.75)
