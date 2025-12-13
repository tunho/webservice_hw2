from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.book import Book, BookStatus
from app.models.user import User, UserRole, UserStatus
from app.core.security import get_password_hash

def test_read_books(client: TestClient, db: Session) -> None:
    # Create book
    book = Book(

        title="Test Book",
        authors="['Test Author']",
        categories="['Fiction']",
        publisher="Test Publisher",
        isbn="1234567890",
        price=10000,
        stock=10,
        publication_date=datetime(2023, 1, 1),
        subcategory="General",
        status=BookStatus.AVAILABLE
    )
    db.add(book)
    db.commit()

    r = client.get(f"{settings.API_V1_STR}/books/")
    assert r.status_code == 200
    content = r.json()
    assert "content" in content
    assert "page" in content
    assert len(content["content"]) > 0
    assert content["content"][0]["title"] == "Test Book"

def test_read_book_by_id(client: TestClient, db: Session) -> None:
    # Create book
    book = Book(

        title="Single Book",
        authors="['Author']",
        categories="['Fiction']",
        publisher="Publisher",
        isbn="0987654321",
        price=20000,
        stock=5,
        publication_date=datetime(2023, 1, 1),
        subcategory="General",
        status=BookStatus.AVAILABLE
    )
    db.add(book)
    db.commit()
    db.refresh(book)

    r = client.get(f"{settings.API_V1_STR}/books/{book.book_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Single Book"

def test_read_book_not_found(client: TestClient) -> None:
    r = client.get(f"{settings.API_V1_STR}/books/99999")
    assert r.status_code == 404
    assert r.json()["code"] == "RESOURCE_NOT_FOUND"
