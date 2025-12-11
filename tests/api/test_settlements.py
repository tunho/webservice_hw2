from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User, UserRole, UserStatus
from app.models.seller import Seller, SellerStatus
from app.models.settlement import Settlement, SettlementStatus
from app.core.security import get_password_hash, create_access_token

def test_create_settlement(client: TestClient, db: Session) -> None:
    # Create seller user and profile
    user = User(
        email="seller_settle@example.com",
        password=get_password_hash("password"),
        name="Seller Settle",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-2222-3333",
        role=UserRole.SELLER,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    db.commit()
    
    seller = Seller(
        user_id=user.user_id,
        business_name="Settle Store",
        business_number="123-45-67890",
        email="seller@store.com",
        phone_number="010-2222-3333",
        address="Seoul",
        payout_bank="Bank",
        payout_account="123456",
        payout_holder="Holder",
        status=SellerStatus.ACTIVE
    )
    db.add(seller)
    db.commit()

    token = create_access_token(user.user_id)
    headers = {"Authorization": f"Bearer {token}"}
    
    settle_data = {
        "period_start": "2023-01-01T00:00:00",
        "period_end": "2023-01-31T23:59:59"
    }

    r = client.post(f"{settings.API_V1_STR}/settlements/", headers=headers, json=settle_data)
    assert r.status_code == 200
    assert r.json()["status"] == "PENDING"

def test_read_settlements(client: TestClient, db: Session) -> None:
    # Create seller and settlement
    user = User(
        email="seller_settle_list@example.com",
        password=get_password_hash("password"),
        name="Seller Settle List",
        birth_date=datetime(1990, 1, 1),
        gender="MALE",
        phone_number="010-2222-4444",
        role=UserRole.SELLER,
        status=UserStatus.ACTIVE
    )
    db.add(user)
    db.commit()
    
    seller = Seller(
        user_id=user.user_id,
        business_name="Settle List Store",
        business_number="123-45-67891",
        email="seller2@store.com",
        phone_number="010-2222-4444",
        address="Seoul",
        payout_bank="Bank",
        payout_account="123456",
        payout_holder="Holder",
        status=SellerStatus.ACTIVE
    )
    db.add(seller)
    db.commit()

    settlement = Settlement(
        seller_id=seller.seller_id,
        period_start=datetime(2023, 1, 1),
        period_end=datetime(2023, 1, 31),
        total_sales=100000,
        commission=10000,
        final_payout=90000,
        status=SettlementStatus.PENDING
    )
    db.add(settlement)
    db.commit()

    token = create_access_token(user.user_id)
    headers = {"Authorization": f"Bearer {token}"}

    r = client.get(f"{settings.API_V1_STR}/settlements/", headers=headers)
    assert r.status_code == 200
    content = r.json()
    assert "content" in content
    assert len(content["content"]) > 0
