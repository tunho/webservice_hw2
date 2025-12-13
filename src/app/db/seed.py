import logging
import json
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole, UserStatus, Gender
from app.models.book import Book, BookStatus
from app.models.cart import Cart, CartStatus
from app.models.cart_item import CartItem
from app.models.order import Order, OrderStatus, PaymentMethod
from app.models.order_item import OrderItem
from app.models.review import Review, ReviewStatus
from app.models.favorite import Favorite

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db: Session) -> None:
    # 1. Create Users
    # Admin
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        admin = User(
            email="admin@example.com",
            password=get_password_hash("admin123"),
            name="Super Admin",
            phone_number="010-0000-0000",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            gender=Gender.MALE,
            birth_date=datetime(1990, 1, 1)
        )
        db.add(admin)
        logger.info("Created Admin User")

    # Customer User
    customer = db.query(User).filter(User.email == "customer@example.com").first()
    if not customer:
        customer = User(
            email="customer@example.com",
            password=get_password_hash("customer123"),
            name="Happy Reader",
            phone_number="010-2222-2222",
            role=UserRole.USER,
            status=UserStatus.ACTIVE,
            gender=Gender.MALE,
            birth_date=datetime(2000, 10, 10)
        )
        db.add(customer)
        logger.info("Created Customer User")

    db.commit()
    
    if customer: db.refresh(customer)



    # 3. Create Books
    books_data = [
        {
            "title": "The Python Journey",
            "subtitle": "From Zero to Hero",
            "authors": ["Guido van Rossum"],
            "publisher": "Tech Press",
            "publication_date": datetime(2023, 1, 15),
            "isbn": "978-3-16-148410-0",
            "description": "Learn Python the right way.",
            "price": 35000,
            "stock_quantity": 100,
            "categories": ["Programming", "Python"],
            "cover_image_url": "https://via.placeholder.com/150"
        },
        {
            "title": "FastAPI Web Development",
            "subtitle": "Building High-Performance APIs",
            "authors": ["Tiangolo"],
            "publisher": "Open Source Books",
            "publication_date": datetime(2023, 6, 20),
            "isbn": "978-1-40-289462-6",
            "description": "Master FastAPI quickly.",
            "price": 42000,
            "stock_quantity": 50,
            "categories": ["Web", "Backend"],
            "cover_image_url": "https://via.placeholder.com/150"
        },
        {
            "title": "Data Science Essentials",
            "subtitle": None,
            "authors": ["Alice Data"],
            "publisher": "Science World",
            "publication_date": datetime(2022, 11, 5),
            "isbn": "978-0-12-345678-9",
            "description": "Introduction to Data Science.",
            "price": 28000,
            "stock_quantity": 200,
            "categories": ["Data Science", "Statistics"],
            "cover_image_url": "https://via.placeholder.com/150"
        }
    ]

    import json
    created_books = []
    for b_data in books_data:
        book = db.query(Book).filter(Book.isbn == b_data["isbn"]).first()
        if not book:
            # Map fields
            book_in = {
                # "seller_id": seller_profile.seller_id, # Removed
                "status": BookStatus.AVAILABLE,
                "title": b_data["title"],
                "authors": json.dumps(b_data["authors"]),
                "categories": json.dumps(b_data["categories"]),
                "publisher": b_data["publisher"],
                "summary": b_data["description"],
                "isbn": b_data["isbn"],
                "price": b_data["price"],
                "stock": b_data["stock_quantity"],
                "cover_image": b_data["cover_image_url"],
                "publication_date": b_data["publication_date"],
                "subcategory": "General" # Default
            }
            book = Book(**book_in)
            db.add(book)
            created_books.append(book)
    
    if created_books:
        db.commit()
        logger.info(f"Created {len(created_books)} Books")
        for b in created_books: db.refresh(b)
    else:
        created_books = db.query(Book).all()

    # 4. Create Cart & Items for Customer
    cart = db.query(Cart).filter(Cart.user_id == customer.user_id, Cart.status == CartStatus.ACTIVE).first()
    if not cart:
        cart = Cart(user_id=customer.user_id, status=CartStatus.ACTIVE)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        
        # Add items
        if len(created_books) >= 2:
            cart_item1 = CartItem(
                cart_id=cart.cart_id,
                book_id=created_books[0].book_id,
                quantity=1,
                unit_price=created_books[0].price,
                subtotal=created_books[0].price
            )
            cart_item2 = CartItem(
                cart_id=cart.cart_id,
                book_id=created_books[1].book_id,
                quantity=2,
                unit_price=created_books[1].price,
                subtotal=created_books[1].price * 2
            )
            db.add(cart_item1)
            db.add(cart_item2)
            db.commit()
            logger.info("Created Cart Items")

    # 5. Create Order for Customer
    from app.models.order import Order, OrderStatus, PaymentMethod
    # Let's assume they bought the 3rd book before
    if len(created_books) >= 3:
        existing_order = db.query(Order).filter(Order.user_id == customer.user_id).first()
        if not existing_order:
            order = Order(
                user_id=customer.user_id,
                total_price=created_books[2].price,
                final_price=created_books[2].price, # No discount
                status=OrderStatus.COMPLETED,
                receiver_name=customer.name,
                receiver_phone=customer.phone_number,
                shipping_address="Seoul, Mapo-gu",
                payment_method=PaymentMethod.CARD
            )
            db.add(order)
            db.commit()
            db.refresh(order)
            
            order_item = OrderItem(
                order_id=order.order_id,
                book_id=created_books[2].book_id,
                quantity=1,
                unit_price=created_books[2].price,
                subtotal=created_books[2].price
            )
            db.add(order_item)
            db.commit()
            logger.info("Created Past Order")

            # 6. Create Review for that book
            review = Review(
                user_id=customer.user_id,
                book_id=created_books[2].book_id,
                rating=5,
                content="Excellent book! Highly recommended.",
                status=ReviewStatus.VISIBLE
            )
            db.add(review)
            db.commit()
            logger.info("Created Review")

    # 7. Create Favorite
    fav = db.query(Favorite).filter(Favorite.user_id == customer.user_id, Favorite.book_id == created_books[0].book_id).first()
    if not fav:
        fav = Favorite(
            user_id=customer.user_id,
            book_id=created_books[0].book_id,
            is_active=True
        )
        db.add(fav)
        db.commit()
        logger.info("Created Favorite")

from app.db.session import SessionLocal, engine
from app.db.base import Base

def main() -> None:
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        init_db(db)
        logger.info("Database seeded successfully!")
        
        # Fetch seller for bulk data
        # seller_user = db.query(User).filter(User.email == "seller@example.com").first()
        # seller_profile = db.query(Seller).filter(Seller.user_id == seller_user.user_id).first()
        
        # if not seller_profile:
        #     print("Error: Seller profile not found for bulk data generation.")
        #     return

        # --- Bulk Data Generation ---
        print("Generating bulk data...")
        
        # 1. Bulk Users (50 Users)
        users = []
        base_time = int(datetime.now().timestamp())
        for i in range(50):
            unique_id = base_time + i
            email = f"user{unique_id}@example.com"
            
            # Check if exists
            existing = db.query(User).filter(User.email == email).first()
            if existing:
                users.append(existing)
                continue
                
            user = User(
                email=email,
                password=get_password_hash("password123"),
                name=f"User {i}",
                birth_date=datetime(1990, 1, 1),
                gender=Gender.MALE if i % 2 == 0 else Gender.FEMALE,
                phone_number=f"010-{unique_id % 10000:04d}-{i:04d}",
                role=UserRole.USER,
                status=UserStatus.ACTIVE
            )
            db.add(user)
            users.append(user)
        db.commit()
        
        # 2. Bulk Books (50 Books)
        books = []
        for i in range(50):
            book = Book(
                # seller_id=seller_profile.seller_id, # Removed
                title=f"Book Title {i}",
                authors=json.dumps([f"Author {i}"]),
                categories=json.dumps(["Fiction", "Adventure"] if i % 2 == 0 else ["Non-fiction", "Science"]),
                publisher=f"Publisher {i}",
                isbn=f"978-00000000{i:02d}",
                price=10000 + (i * 100),
                stock=100,
                publication_date=datetime.now(),
                subcategory="General",
                status=BookStatus.AVAILABLE
            )
            db.add(book)
            books.append(book)
        db.commit()
        
        # 3. Bulk Orders (100 Orders)
        for i in range(100):
            user = users[i % len(users)]
            book = books[i % len(books)]
            
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
            
            # 4. Bulk Reviews (Linked to orders/books)
            review = Review(
                user_id=user.user_id,
                book_id=book.book_id,
                rating=5 if i % 2 == 0 else 4,
                content=f"Great book! Review number {i}",
                status=ReviewStatus.VISIBLE
            )
            db.add(review)
            
        db.commit()
        print("Bulk data generation complete!")
    finally:
        db.close()

if __name__ == "__main__":
    main()
