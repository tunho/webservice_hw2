from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.book_discount import BookDiscountStatus

class DiscountBase(BaseModel):
    book_id: int
    discount_rate: int
    start_at: datetime
    end_at: datetime

class DiscountCreate(DiscountBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "book_id": 1,
                "discount_rate": 20,
                "start_at": "2025-01-01T00:00:00",
                "end_at": "2025-01-07T23:59:59"
            }
        }
    )

class DiscountUpdate(BaseModel):
    discount_rate: Optional[int] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    status: Optional[BookDiscountStatus] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "discount_rate": 30,
                "end_at": "2025-01-14T23:59:59"
            }
        }
    )

class DiscountResponse(DiscountBase):
    discount_id: int
    status: BookDiscountStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "book_id": 1,
                "discount_rate": 20,
                "start_at": "2025-01-01T00:00:00",
                "end_at": "2025-01-07T23:59:59",
                "discount_id": 1,
                "status": "ACTIVE",
                "created_at": "2025-01-01T00:00:00"
            }
        }
    )
