from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class PaymentRequest(BaseModel):
    order_number: str
    customer_id: int
    amount: float
    timestamp: str


class PaymentProcessRequest(BaseModel):
    order_number: str
    customer_id: int
    amount: float
    payment_method: Optional[str] = "CARD"


class PaymentResponse(BaseModel):
    transaction_id: str
    order_number: str
    amount: float
    payment_status: str
    message: str


class PaymentStatusUpdate(BaseModel):
    transaction_id: str
    status: str


class PaymentDBResponse(BaseModel):
    id: int
    order_number: str
    customer_id: int
    amount: float
    transaction_id: str
    payment_status: str
    payment_method: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WebhookPayload(BaseModel):
    order_number: str
    status: str
    transaction_id: str