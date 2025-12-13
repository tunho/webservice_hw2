from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User, UserRole, UserStatus
from app.models.book import Book, BookStatus
from app.core.security import get_password_hash, create_access_token

def test_create_order(client: TestClient, db: Session) -> None:
    # Create user
    user = User(
        email="order_user@example.com",
        password=get_password_hash("password"),
        name="Order User",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-1111-2222",
        role=UserRole.USER,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    
    # Create book
    book = Book(

        title="Order Book",
        authors="['Author']",
        categories="['Fiction']",
        publisher="Publisher",
        isbn="1122334455",
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
    
    order_data = {
        "items": [{
            "book_id": book.book_id, 
            "quantity": 1,
            "unit_price": 10000,
            "subtotal": 10000
        }],
        "payment_method": "CARD",
        "receiver_name": "Receiver",
        "receiver_phone": "010-1111-2222",
        "shipping_address": "Address"
    }

    r = client.post(f"{settings.API_V1_STR}/orders/", headers=headers, json=order_data)
    assert r.status_code == 200
    assert r.json()["total_price"] == 10000

def test_read_orders(client: TestClient, db: Session) -> None:
    # Create user
    user = User(
        email="order_list_user@example.com",
        password=get_password_hash("password"),
        name="Order List User",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-3333-4444",
        role=UserRole.USER,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    db.commit()

    token = create_access_token(user.user_id)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.get(f"{settings.API_V1_STR}/orders/", headers=headers)
    assert r.status_code == 200
    content = r.json()
    assert "content" in content
    assert len(content["content"]) == 0 # No orders yet
