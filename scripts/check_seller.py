from app.db.session import SessionLocal
from app.models.user import User
from app.models.seller import Seller

db = SessionLocal()
try:
    user = db.query(User).filter(User.user_id == 3).first()
    if user:
        print(f"User ID 3: {user.email}, Role: {user.role}")
        seller = db.query(Seller).filter(Seller.user_id == 3).first()
        if seller:
            print(f"Seller Profile: Found (ID: {seller.seller_id})")
        else:
            print("Seller Profile: NOT FOUND")
    else:
        print("User ID 3: NOT FOUND")
        
    # Check if any seller exists
    all_sellers = db.query(Seller).all()
    print(f"Total Sellers in DB: {len(all_sellers)}")
    for s in all_sellers:
        print(f" - Seller ID: {s.seller_id}, User ID: {s.user_id}")

finally:
    db.close()
