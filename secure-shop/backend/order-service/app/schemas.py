from pydantic import BaseModel
from pydantic import ConfigDict

from typing import List

class OrderItem(BaseModel):
    name: str
    quantity: int

class CreateOrderRequest(BaseModel):
    items: List[OrderItem]

class OrderResponse(BaseModel):
    order_number: str
    customer_name: str
    total_amount: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class PaymentResponse(BaseModel):
    transaction_id: str
    payment_status: str

class MessageResponse(BaseModel):
    message: str