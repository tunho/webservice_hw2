from app.db.session import SessionLocal
from app.models.user import User, UserRole, UserStatus, Gender
from app.core.security import get_password_hash
from datetime import datetime

db = SessionLocal()

admin = db.query(User).filter(User.email == "admin@example.com").first()

if admin:
    print(f"Admin user found. Status: {admin.status}")
    if admin.status != UserStatus.ACTIVE:
        admin.status = UserStatus.ACTIVE
        db.add(admin)
        db.commit()
        print("Admin user reactivated.")
    else:
        print("Admin user is already active.")
else:
    print("Admin user not found. Creating new admin user...")
    admin = User(
        email="admin@example.com",
        password=get_password_hash("admin123"),
        name="Super Admin",
        nickname="Admin",
        phone_number="010-0000-0000",
        role=UserRole.ADMIN,
        status=UserStatus.ACTIVE,
        gender=Gender.MALE,
        birth_date=datetime(1990, 1, 1),
        address="Seoul, Gangnam-gu",
        region="KR"
    )
    db.add(admin)
    db.commit()
    print("Admin user created.")

db.close()
