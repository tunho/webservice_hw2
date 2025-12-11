from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User, UserRole, UserStatus
from app.core.security import get_password_hash

def test_login_access_token(client: TestClient, db: Session) -> None:
    # Create user
    email = "test@example.com"
    password = "password"
    user = User(
        email=email,
        password=get_password_hash(password),
        name="Test User",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-1234-5678",
        role=UserRole.USER,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    db.commit()

    login_data = {
        "username": email,
        "password": password,
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]

def test_login_incorrect_password(client: TestClient, db: Session) -> None:
    # Create user
    email = "test2@example.com"
    password = "password"
    user = User(
        email=email,
        password=get_password_hash(password),
        name="Test User 2",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-1234-5679",
        role=UserRole.USER,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    db.commit()

    login_data = {
        "username": email,
        "password": "wrongpassword",
    }
    r = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert r.status_code == 400
    assert r.json()["code"] == "BAD_REQUEST" # Based on our exception handler
