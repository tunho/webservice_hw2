from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()
admin = db.query(User).filter(User.email == "admin@example.com").first()

if admin:
    print(f"Old Hash: {admin.password}")
    new_hash = get_password_hash("admin123")
    admin.password = new_hash
    db.add(admin)
    db.commit()
    print(f"New Hash: {admin.password}")
    print("Admin password updated to 'admin123'")
else:
    print("Admin user NOT found")
