from app.db.session import SessionLocal
from app.models.user import User
from app.models.seller import Seller
from app.core.security import verify_password

db = SessionLocal()
try:
    email = "seller@example.com"
    user = db.query(User).filter(User.email == email).first()
    if user:
        print(f"User Found: ID {user.user_id}, Role: {user.role}")
        seller = db.query(Seller).filter(Seller.user_id == user.user_id).first()
        if seller:
            print(f"Seller Profile Found: ID {seller.seller_id}")
        else:
            print("Seller Profile: NOT FOUND")
            
        # Check password
        is_valid = verify_password("seller123", user.password)
        print(f"Password 'seller123' valid: {is_valid}")
    else:
        print(f"User {email} NOT FOUND")

finally:
    db.close()
