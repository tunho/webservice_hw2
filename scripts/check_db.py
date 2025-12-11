from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import verify_password, get_password_hash

db = SessionLocal()
admin = db.query(User).filter(User.email == "admin@example.com").first()

if admin:
    print(f"Admin found: {admin.email}")
    print(f"Hashed Password in DB: {admin.password}")
    print(f"User Status: {admin.status}")
    
    is_valid = verify_password("admin123", admin.password)
    print(f"Is 'admin123' valid? {is_valid}")
    
    new_hash = get_password_hash("admin123")
    print(f"New hash of 'admin123': {new_hash}")
    print(f"Is new hash valid? {verify_password('admin123', new_hash)}")
else:
    print("Admin user NOT found in DB")
