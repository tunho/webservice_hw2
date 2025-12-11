from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.book import BookStatus

class BookBase(BaseModel):
    title: str
    authors: str # JSON string or List? Schema says text (JSON array). Let's accept string for now or List if we parse it.
    categories: str # JSON string
    publisher: str
    summary: Optional[str] = None
    isbn: str
    price: int
    stock: int
    cover_image: Optional[str] = None
    publication_date: datetime
    subcategory: str

class BookCreate(BookBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "The Great Gatsby",
                "authors": "[\"F. Scott Fitzgerald\"]",
                "categories": "[\"Fiction\", \"Classic\"]",
                "publisher": "Scribner",
                "summary": "A novel about the American dream.",
                "isbn": "978-0743273565",
                "price": 15000,
                "stock": 100,
                "cover_image": "http://example.com/gatsby.jpg",
                "publication_date": "1925-04-10T00:00:00",
                "subcategory": "Classic Literature"
            }
        }
    )

class BookUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
    stock: Optional[int] = None
    status: Optional[BookStatus] = None
    discount_rate: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "price": 12000,
                "stock": 90,
                "discount_rate": 10
            }
        }
    )

class BookResponse(BookBase):
    book_id: int
    seller_id: int
    discount_rate: int
    average_rating: float
    review_count: int
    status: BookStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "title": "The Great Gatsby",
                "authors": "[\"F. Scott Fitzgerald\"]",
                "categories": "[\"Fiction\", \"Classic\"]",
                "publisher": "Scribner",
                "summary": "A novel about the American dream.",
                "isbn": "978-0743273565",
                "price": 15000,
                "stock": 100,
                "cover_image": "http://example.com/gatsby.jpg",
                "publication_date": "1925-04-10T00:00:00",
                "subcategory": "Classic Literature",
                "book_id": 1,
                "seller_id": 1,
                "discount_rate": 0,
                "average_rating": 4.5,
                "review_count": 10,
                "status": "ON_SALE",
                "created_at": "2025-01-01T00:00:00",
                "updated_at": "2025-01-01T00:00:00"
            }
        }
    )
