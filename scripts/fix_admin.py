from app.db.session import SessionLocal
from app.models.user import User, UserStatus
from app.core.security import get_password_hash

db = SessionLocal()
admin = db.query(User).filter(User.email == "admin@example.com").first()

if admin:
    print(f"Current Status: {admin.status}")
    admin.status = UserStatus.ACTIVE
    # Ensure password is correct too
    admin.password = get_password_hash("admin123")
    
    db.add(admin)
    db.commit()
    print(f"New Status: {admin.status}")
    print("Admin status updated to ACTIVE and password to 'admin123'")
else:
    print("Admin user NOT found")
