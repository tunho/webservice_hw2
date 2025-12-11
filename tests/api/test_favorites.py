from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User, UserRole, UserStatus
from app.models.book import Book, BookStatus
from app.models.favorite import Favorite
from app.core.security import get_password_hash, create_access_token

def test_create_favorite(client: TestClient, db: Session) -> None:
    # Create user
    user = User(
        email="fav_user@example.com",
        password=get_password_hash("password"),
        name="Fav User",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-4444-5555",
        role=UserRole.USER,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    
    book = Book(
        seller_id=1,
        title="Fav Book",
        authors="['Author']",
        categories="['Fiction']",
        publisher="Publisher",
        isbn="4455667788",
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
    
    fav_data = {
        "book_id": book.book_id
    }

    r = client.post(f"{settings.API_V1_STR}/favorites/", headers=headers, json=fav_data)
    assert r.status_code == 200
    assert r.json()["book_id"] == book.book_id

def test_read_favorites(client: TestClient, db: Session) -> None:
    # Create user and favorite
    user = User(
        email="fav_list_user@example.com",
        password=get_password_hash("password"),
        name="Fav List User",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-4444-6666",
        role=UserRole.USER,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    db.commit() # Need user_id

    favorite = Favorite(
        user_id=user.user_id,
        book_id=1, # Mock
        is_active=True
    )
    db.add(favorite)
    db.commit()

    token = create_access_token(user.user_id)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.get(f"{settings.API_V1_STR}/favorites/", headers=headers)
    assert r.status_code == 200
    content = r.json()
    assert "content" in content
    assert len(content["content"]) > 0

def test_delete_favorite(client: TestClient, db: Session) -> None:
    # Create user and favorite
    user = User(
        email="fav_del_user@example.com",
        password=get_password_hash("password"),
        name="Fav Del User",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-4444-7777",
        role=UserRole.USER,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    db.commit()

    book = Book(
        seller_id=1,
        title="Fav Del Book",
        authors="['Author']",
        categories="['Fiction']",
        publisher="Publisher",
        isbn="4455667799",
        price=10000,
        stock=10,
        publication_date=datetime(2023, 1, 1),
        subcategory="General",
        status=BookStatus.AVAILABLE
    )
    db.add(book)
    db.commit()

    favorite = Favorite(
        user_id=user.user_id,
        book_id=book.book_id,
        is_active=True
    )
    db.add(favorite)
    db.commit()

    token = create_access_token(user.user_id)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.delete(f"{settings.API_V1_STR}/favorites/{book.book_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["message"] == "Favorite removed (soft deleted)"
