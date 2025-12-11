from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User, UserRole, UserStatus
from app.models.book import Book, BookStatus
from app.models.book_discount import BookDiscount, BookDiscountStatus
from app.core.security import get_password_hash, create_access_token

def test_create_discount(client: TestClient, db: Session) -> None:
    # Create seller user
    user = User(
        email="seller_discount@example.com",
        password=get_password_hash("password"),
        name="Seller Discount",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-6666-7777",
        role=UserRole.SELLER,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    
    book = Book(
        seller_id=1,
        title="Discount Book",
        authors="['Author']",
        categories="['Fiction']",
        publisher="Publisher",
        isbn="6677889900",
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
    
    discount_data = {
        "book_id": book.book_id,
        "discount_rate": 10, # Integer 0-100
        "start_at": "2023-01-01T00:00:00",
        "end_at": "2023-12-31T23:59:59"
    }

    r = client.post(f"{settings.API_V1_STR}/discounts/", headers=headers, json=discount_data)
    assert r.status_code == 200
    assert r.json()["discount_rate"] == 10

def test_read_discounts(client: TestClient, db: Session) -> None:
    # Create discount
    discount = BookDiscount(
        book_id=1, # Mock
        discount_rate=20,
        start_at=datetime(2023, 1, 1),
        end_at=datetime(2023, 12, 31),
        status=BookDiscountStatus.ACTIVE
    )
    db.add(discount)
    db.commit()

    r = client.get(f"{settings.API_V1_STR}/discounts/")
    assert r.status_code == 200
    content = r.json()
    assert "content" in content
