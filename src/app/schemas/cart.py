from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class CartItemBase(BaseModel):
    book_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "book_id": 1,
                "quantity": 1
            }
        }
    )

class CartItemResponse(CartItemBase):
    cart_item_id: int
    unit_price: int
    subtotal: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "book_id": 1,
                "quantity": 2,
                "cart_item_id": 1,
                "unit_price": 15000,
                "subtotal": 30000
            }
        }
    )

class CartResponse(BaseModel):
    cart_id: int
    total_amount: int
    items: List[CartItemResponse] = []

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "cart_id": 1,
                "total_amount": 30000,
                "items": [
                    {
                        "book_id": 1,
                        "quantity": 2,
                        "cart_item_id": 1,
                        "unit_price": 15000,
                        "subtotal": 30000
                    }
                ]
            }
        }
    )
