from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.seller import SellerStatus

class SellerBase(BaseModel):
    business_name: str
    business_number: str
    email: str
    phone_number: str
    address: str
    payout_bank: str
    payout_account: str
    payout_holder: str

class SellerCreate(SellerBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "business_name": "Best Books Inc.",
                "business_number": "123-45-67890",
                "email": "seller@example.com",
                "phone_number": "02-1234-5678",
                "address": "Seoul, Korea",
                "payout_bank": "K-Bank",
                "payout_account": "123-456-789012",
                "payout_holder": "Hong Gildong"
            }
        }
    )

class SellerUpdate(BaseModel):
    business_name: Optional[str] = None
    business_number: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    payout_bank: Optional[str] = None
    payout_account: Optional[str] = None
    payout_holder: Optional[str] = None
    status: Optional[SellerStatus] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "phone_number": "02-9876-5432",
                "address": "Busan, Korea"
            }
        }
    )

class SellerResponse(SellerBase):
    seller_id: int
    user_id: int
    status: SellerStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "business_name": "Best Books Inc.",
                "business_number": "123-45-67890",
                "email": "seller@example.com",
                "phone_number": "02-1234-5678",
                "address": "Seoul, Korea",
                "payout_bank": "K-Bank",
                "payout_account": "123-456-789012",
                "payout_holder": "Hong Gildong",
                "seller_id": 1,
                "user_id": 1,
                "status": "APPROVED",
                "created_at": "2025-01-01T00:00:00"
            }
        }
    )
