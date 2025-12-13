from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.order import OrderStatus, PaymentMethod

from pydantic import BaseModel, ConfigDict, Field

class OrderItemSchema(BaseModel):
    book_id: int
    quantity: int
    unit_price: int
    subtotal: int

    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    payment_method: PaymentMethod
    receiver_name: str
    receiver_phone: str
    shipping_address: str

class OrderCreate(OrderBase):
    items: List[OrderItemSchema] = Field(min_length=1) # Simplified for creation

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_method": "CARD",
                "receiver_name": "John Doe",
                "receiver_phone": "010-1234-5678",
                "shipping_address": "Seoul, Korea",
                "items": [
                    {
                        "book_id": 1,
                        "quantity": 1,
                        "unit_price": 15000,
                        "subtotal": 15000
                    }
                ]
            }
        }
    )

class OrderResponse(OrderBase):
    order_id: int
    user_id: int
    total_price: int
    discount_amount: int
    final_price: int
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemSchema] = []
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "payment_method": "CARD",
                "receiver_name": "John Doe",
                "receiver_phone": "010-1234-5678",
                "shipping_address": "Seoul, Korea",
                "order_id": 1,
                "user_id": 1,
                "total_price": 15000,
                "discount_amount": 1000,
                "final_price": 15000,
                "status": "CREATED",
                "created_at": "2025-01-01T00:00:00"
            }
        }
    )
