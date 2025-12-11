from app.db.session import SessionLocal
from app.models.review import Review
from app.models.user import User
from app.models.book import Book
from app.models.seller import Seller

db = SessionLocal()
reviews = db.query(Review).all()

print(f"Total Reviews: {len(reviews)}")
for r in reviews[:5]:
    print(f"ID: {r.review_id}, Content: {r.content}")
