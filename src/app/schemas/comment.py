from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "content": "Great post! Thanks for sharing."
            }
        }
    )

class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "content": "Great post! Thanks for sharing.",
                "id": 1,
                "post_id": 1,
                "user_id": 1,
                "created_at": "2025-01-01T00:00:00"
            }
        }
    )
