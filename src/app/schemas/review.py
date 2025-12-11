from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ReviewBase(BaseModel):
    rating: int
    content: str

class ReviewCreate(ReviewBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "rating": 5,
                "content": "This book was amazing! Highly recommended."
            }
        }
    )

class ReviewResponse(ReviewBase):
    review_id: int
    user_id: int
    book_id: int
    like_count: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "rating": 5,
                "content": "This book was amazing! Highly recommended.",
                "review_id": 1,
                "user_id": 1,
                "book_id": 1,
                "like_count": 10,
                "created_at": "2025-01-01T00:00:00"
            }
        }
    )
