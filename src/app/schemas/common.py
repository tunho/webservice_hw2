from typing import Generic, TypeVar, List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime

T = TypeVar("T")

class ErrorResponse(BaseModel):
    timestamp: datetime
    path: str
    status: int
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class PageResponse(BaseModel, Generic[T]):
    content: List[T]
    page: int
    size: int
    totalElements: int
    totalPages: int
    sort: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "content": [
                    {
                        "id": 1,
                        "name": "Example Item"
                    }
                ],
                "page": 0,
                "size": 20,
                "totalElements": 100,
                "totalPages": 5,
                "sort": "created_at,desc"
            }
        }
    )
