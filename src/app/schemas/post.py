from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    category_id: int

class PostCreate(PostBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "My First Post",
                "content": "Hello world! This is my first post.",
                "category_id": 1
            }
        }
    )

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Updated Title",
                "content": "Updated content."
            }
        }
    )

class PostResponse(PostBase):
    id: int
    user_id: int
    view_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
