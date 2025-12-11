from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User, UserRole, UserStatus
from app.models.book import Book, BookStatus
from app.models.review import Review, ReviewStatus
from app.core.security import get_password_hash, create_access_token

def test_create_review(client: TestClient, db: Session) -> None:
    # Create user
    user = User(
        email="review_user@example.com",
        password=get_password_hash("password"),
        name="Review User",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-5555-6666",
        role=UserRole.USER,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    
    # Create book
    book = Book(
        seller_id=1,
        title="Review Book",
        authors="['Author']",
        categories="['Fiction']",
        publisher="Publisher",
        isbn="5566778899",
        price=10000,
        stock=10,
        publication_date=datetime(2023, 1, 1),
        subcategory="General",
        status=BookStatus.AVAILABLE
    )
    db.add(book)
    db.commit()

    token = create_access_token(user.user_id)
    headers = {"Authorization": f"Bearer {token}"}
    
    review_data = {
        "rating": 5,
        "content": "Great book!"
    }

    r = client.post(f"{settings.API_V1_STR}/reviews/{book.book_id}", headers=headers, json=review_data)
    assert r.status_code == 200
    assert r.json()["rating"] == 5

def test_read_reviews(client: TestClient, db: Session) -> None:
    # Create book
    book = Book(
        seller_id=1,
        title="Review List Book",
        authors="['Author']",
        categories="['Fiction']",
        publisher="Publisher",
        isbn="9988776655",
        price=10000,
        stock=10,
        publication_date=datetime(2023, 1, 1),
        subcategory="General",
        status=BookStatus.AVAILABLE
    )
    db.add(book)
    db.commit()

    r = client.get(f"{settings.API_V1_STR}/reviews/{book.book_id}")
    assert r.status_code == 200
    content = r.json()
    assert "content" in content
