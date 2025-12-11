from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.settlement import SettlementStatus

class SettlementBase(BaseModel):
    period_start: datetime
    period_end: datetime

class SettlementCreate(SettlementBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "period_start": "2025-01-01T00:00:00",
                "period_end": "2025-01-31T23:59:59"
            }
        }
    )

class SettlementUpdate(BaseModel):
    status: Optional[SettlementStatus] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "COMPLETED"
            }
        }
    )

class SettlementResponse(SettlementBase):
    settlement_id: int
    seller_id: int
    total_sales: int
    commission: int
    final_payout: int
    status: SettlementStatus
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "period_start": "2025-01-01T00:00:00",
                "period_end": "2025-01-31T23:59:59",
                "settlement_id": 1,
                "seller_id": 1,
                "total_sales": 1000000,
                "commission": 100000,
                "final_payout": 900000,
                "status": "COMPLETED",
                "created_at": "2025-02-01T00:00:00"
            }
        }
    )
