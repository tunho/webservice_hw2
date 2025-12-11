from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class FavoriteBase(BaseModel):
    book_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteResponse(FavoriteBase):
    favorite_id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "book_id": 1,
                "favorite_id": 1,
                "user_id": 1,
                "created_at": "2025-01-01T00:00:00"
            }
        }
    )
