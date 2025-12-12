from sqlalchemy import Integer, Column, Integer, String, Text, ForeignKey, DateTime, Enum, BigInteger, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class BookStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    SOLD_OUT = "SOLD_OUT"
    DISCONTINUED = "DISCONTINUED"
    DELETED = "DELETED"

class Book(Base):
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(Integer, ForeignKey("seller.seller_id"), nullable=False)
    
    title = Column(String(255), nullable=False)
    authors = Column(Text, nullable=False) # JSON array
    categories = Column(Text, nullable=False) # JSON array
    publisher = Column(String(150), nullable=False)
    summary = Column(Text, nullable=True)
    isbn = Column(String(13), unique=True, nullable=False)
    
    price = Column(Integer, nullable=False)
    discount_rate = Column(Integer, default=0)
    stock = Column(Integer, default=0)
    average_rating = Column(Numeric(2, 1), default=0.0)
    review_count = Column(Integer, default=0)
    
    cover_image = Column(String(255), nullable=True)
    publication_date = Column(DateTime, nullable=False)
    
    status = Column(Enum(BookStatus), default=BookStatus.AVAILABLE, nullable=False)
    subcategory = Column(String(100), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    seller = relationship("Seller", backref="books")
