from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    purchase_year: int = Field(..., json_schema_extra={"example": 2018})
    purchase_month: int = Field(..., ge=1, le=12, json_schema_extra={"example": 5})
    purchase_day: int = Field(..., ge=1, le=31, json_schema_extra={"example": 15})
    purchase_hour: int = Field(..., ge=0, le=23, json_schema_extra={"example": 12})
    purchase_dayofweek: int = Field(..., ge=0, le=6, json_schema_extra={"example": 2})
    customer_state: str = Field(..., json_schema_extra={"example": "SP"})
    n_items: int = Field(..., ge=1, json_schema_extra={"example": 2})
    n_unique_products: int = Field(..., ge=1, json_schema_extra={"example": 2})
    n_unique_sellers: int = Field(..., ge=1, json_schema_extra={"example": 1})
    payment_installments_max: int = Field(..., ge=1, json_schema_extra={"example": 3})


class PredictResponse(BaseModel):
    prediction: float = Field(..., json_schema_extra={"example": 149.75})
