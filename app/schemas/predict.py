from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    purchase_month: int = Field(..., ge=1, le=12, json_schema_extra={"example": 5})
    purchase_dayofweek: int = Field(..., ge=0, le=6, json_schema_extra={"example": 2})
    customer_state: str = Field(..., json_schema_extra={"example": "SP"})
    customer_city: str = Field(..., json_schema_extra={"example": "sao paulo"})
    payment_installments: int = Field(..., ge=1, json_schema_extra={"example": 3})
    items_count: int = Field(..., ge=1, json_schema_extra={"example": 2})
    freight_value: float = Field(..., ge=0, json_schema_extra={"example": 21.5})
    review_score: float = Field(..., ge=1, le=5, json_schema_extra={"example": 4.0})
    delivery_delay_days: int = Field(..., json_schema_extra={"example": 0})


class PredictResponse(BaseModel):
    prediction: float = Field(..., json_schema_extra={"example": 149.75})
