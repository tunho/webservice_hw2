from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User, UserRole, UserStatus
from app.core.security import get_password_hash, create_access_token

def test_read_users_superuser(client: TestClient, db: Session) -> None:
    # Create superuser
    email = "admin@example.com"
    password = "password"
    user = User(
        email=email,
        password=get_password_hash(password),
        name="Admin User",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-9999-9999",
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    db.commit()

    token = create_access_token(user.user_id)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.get(f"{settings.API_V1_STR}/users/", headers=headers)
    assert r.status_code == 200
    content = r.json()
    assert "content" in content
    assert len(content["content"]) > 0

def test_read_users_normal_user(client: TestClient, db: Session) -> None:
    # Create normal user
    email = "user@example.com"
    password = "password"
    user = User(
        email=email,
        password=get_password_hash(password),
        name="Normal User",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-8888-8888",
        role=UserRole.USER,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    db.commit()

    token = create_access_token(user.user_id)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.get(f"{settings.API_V1_STR}/users/", headers=headers)
    # Assuming only admin can list users
    assert r.status_code == 400 # Or 403 depending on implementation
    assert r.json()["code"] == "BAD_REQUEST"
