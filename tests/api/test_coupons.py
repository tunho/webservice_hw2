from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User, UserRole, UserStatus
from app.models.coupon import Coupon
from app.core.security import get_password_hash, create_access_token

def test_create_coupon(client: TestClient, db: Session) -> None:
    # Create admin user
    user = User(
        email="admin_coupon@example.com",
        password=get_password_hash("password"),
        name="Admin Coupon",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-7777-8888",
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    db.commit()

    token = create_access_token(user.user_id)
    headers = {"Authorization": f"Bearer {token}"}
    
    coupon_data = {
        "code": "TESTCOUPON",
        "name": "Test Coupon",
        "discount_rate": 10,
        "min_order": 1000,
        "max_discount": 5000,
        "start_date": "2023-01-01T00:00:00",
        "end_date": "2023-12-31T23:59:59"
    }

    r = client.post(f"{settings.API_V1_STR}/coupons/", headers=headers, json=coupon_data)
    assert r.status_code == 200
    assert r.json()["code"] == "TESTCOUPON"

def test_read_coupons(client: TestClient, db: Session) -> None:
    # Create coupon
    coupon = Coupon(
        code="LISTCOUPON",
        name="List Coupon",
        discount_rate=10,
        min_order=1000,
        max_discount=5000,
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31)
    )
    db.add(coupon)
    db.commit()

    r = client.get(f"{settings.API_V1_STR}/coupons/")
    assert r.status_code == 200
    content = r.json()
    assert "content" in content
    assert len(content["content"]) > 0

def test_delete_coupon(client: TestClient, db: Session) -> None:
    # Create admin user
    user = User(
        email="admin_del_coupon@example.com",
        password=get_password_hash("password"),
        name="Admin Del Coupon",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-7777-9999",
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    
    coupon = Coupon(
        code="DELCOUPON",
        name="Del Coupon",
        discount_rate=10,
        min_order=1000,
        max_discount=5000,
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 12, 31)
    )
    db.add(coupon)
    db.commit()

    token = create_access_token(user.user_id)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.delete(f"{settings.API_V1_STR}/coupons/{coupon.coupon_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["message"] == "Coupon deleted"
