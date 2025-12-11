from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import verify_password, get_password_hash

db = SessionLocal()
admin = db.query(User).filter(User.email == "admin@example.com").first()

if admin:
    print(f"Admin found. Status: {admin.status}")
    if verify_password("admin123", admin.password):
        print("Password 'admin123' is CORRECT.")
    else:
        print("Password 'admin123' is INCORRECT.")
        # Fix it
        admin.password = get_password_hash("admin123")
        db.add(admin)
        db.commit()
        print("Password has been reset to 'admin123'.")
else:
    print("Admin user not found.")
