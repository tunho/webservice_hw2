import logging
import json
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.core.security import get_password_hash
from app.models.user import User, UserRole, UserStatus, Gender
from app.models.book import Book, BookStatus
from app.models.cart import Cart, CartStatus
from app.models.cart_item import CartItem
from app.models.order import Order, OrderStatus, PaymentMethod
from app.models.order_item import OrderItem
from app.models.review import Review, ReviewStatus
from app.models.favorite import Favorite
from app.db.seed import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main() -> None:
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Run basic init first (Admin, basic users)
        init_db(db)
        logger.info("Basic seed data created.")
        
        # --- Bulk Data Generation (Large Scale) ---
        NUM_USERS = 1000
        NUM_BOOKS = 1000
        NUM_ORDERS = 5000
        
        print(f"Generating bulk data: {NUM_USERS} Users, {NUM_BOOKS} Books, {NUM_ORDERS} Orders...")
        
        # 1. Bulk Users
        users = []
        base_time = int(datetime.now().timestamp())
        
        # Check existing count to avoid duplicates if run multiple times
        existing_users_count = db.query(User).count()
        start_idx = existing_users_count
        
        for i in range(start_idx, start_idx + NUM_USERS):
            unique_id = base_time + i
            email = f"user_large_{unique_id}@example.com"
            
            user = User(
                email=email,
                password=get_password_hash("password123"),
                name=f"User {i}",
                birth_date=datetime(1990, 1, 1),
                gender=Gender.MALE if i % 2 == 0 else Gender.FEMALE,
                phone_number=f"010-{unique_id % 10000:04d}-{i % 10000:04d}",
                role=UserRole.USER,
                status=UserStatus.ACTIVE
            )
            db.add(user)
            users.append(user)
            
            if len(users) % 100 == 0:
                db.commit()
                print(f"Created {len(users)} users...")
        db.commit()
        # Reload all users for order generation
        all_users = db.query(User).filter(User.role == UserRole.USER).all()
        
        # 2. Bulk Books
        books = []
        existing_books_count = db.query(Book).count()
        start_book_idx = existing_books_count
        
        for i in range(start_book_idx, start_book_idx + NUM_BOOKS):
            book = Book(
                title=f"Large Scale Book Title {i}",
                authors=json.dumps([f"Author {i}"]),
                categories=json.dumps(["Fiction", "Adventure"] if i % 2 == 0 else ["Non-fiction", "Science"]),
                publisher=f"Publisher {i}",
                isbn=f"978-LARGE-{i:06d}",
                price=10000 + (i * 10),
                stock=1000,
                publication_date=datetime.now(),
                subcategory="General",
                status=BookStatus.AVAILABLE
            )
            db.add(book)
            books.append(book)
            
            if len(books) % 100 == 0:
                db.commit()
                print(f"Created {len(books)} books...")
        db.commit()
        # Reload all books
        all_books = db.query(Book).all()
        
        # 3. Bulk Orders
        print("Creating orders...")
        for i in range(NUM_ORDERS):
            user = random.choice(all_users)
            book = random.choice(all_books)
            
            order = Order(
                user_id=user.user_id,
                payment_method=PaymentMethod.CARD,
                receiver_name=user.name,
                receiver_phone=user.phone_number,
                shipping_address="Seoul, Korea",
                total_price=book.price,
                final_price=book.price,
                status=OrderStatus.COMPLETED
            )
            db.add(order)
            db.flush()
            
            order_item = OrderItem(
                order_id=order.order_id,
                book_id=book.book_id,
                quantity=1,
                unit_price=book.price,
                subtotal=book.price
            )
            db.add(order_item)
            
            # Randomly add review (30% chance)
            if random.random() < 0.3:
                review = Review(
                    user_id=user.user_id,
                    book_id=book.book_id,
                    rating=random.randint(1, 5),
                    content=f"Review for book {book.book_id} by user {user.user_id}",
                    status=ReviewStatus.VISIBLE
                )
                db.add(review)
            
            if i % 100 == 0:
                db.commit()
                print(f"Created {i} orders...")
                
        db.commit()
        print("Large scale data generation complete!")
    finally:
        db.close()

if __name__ == "__main__":
    main()
