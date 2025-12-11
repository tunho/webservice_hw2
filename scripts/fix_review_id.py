from app.db.session import SessionLocal
from app.models.review import Review, ReviewStatus
from app.models.user import User
from app.models.book import Book
from app.models.seller import Seller

db = SessionLocal()

# Check if ID 1 exists
review = db.query(Review).filter(Review.review_id == 1).first()

if not review:
    print("Review ID 1 not found. Creating it...")
    # Need a user and a book
    user = db.query(User).first()
    book = db.query(Book).first()
    
    if user and book:
        review = Review(
            review_id=1, # Force ID 1
            user_id=user.user_id,
            book_id=book.book_id,
            rating=5,
            content="Restored Review ID 1",
            status=ReviewStatus.VISIBLE
        )
        db.add(review)
        db.commit()
        print("Successfully created Review ID 1")
    else:
        print("Error: No user or book found to link review to.")
else:
    print("Review ID 1 already exists.")
