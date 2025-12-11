from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.coupon import CouponStatus

class CouponBase(BaseModel):
    code: str
    name: str
    discount_rate: int
    min_order: int
    max_discount: int
    start_date: datetime
    end_date: datetime

class CouponCreate(CouponBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": "WELCOME2025",
                "name": "New Year Sale",
                "discount_rate": 10,
                "min_order": 20000,
                "max_discount": 5000,
                "start_date": "2025-01-01T00:00:00",
                "end_date": "2025-01-31T23:59:59"
            }
        }
    )

class CouponResponse(CouponBase):
    coupon_id: int
    status: CouponStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "code": "WELCOME2025",
                "name": "New Year Sale",
                "discount_rate": 10,
                "min_order": 20000,
                "max_discount": 5000,
                "start_date": "2025-01-01T00:00:00",
                "end_date": "2025-01-31T23:59:59",
                "coupon_id": 1,
                "status": "ACTIVE",
                "created_at": "2025-01-01T00:00:00"
            }
        }
    )
