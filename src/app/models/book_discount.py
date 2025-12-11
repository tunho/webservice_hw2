import enum
from sqlalchemy import Integer, Column, Integer, ForeignKey, Boolean, DateTime, BigInteger, CheckConstraint, Enum
from sqlalchemy.sql import func
from app.db.base_class import Base

class BookDiscountStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    DELETED = "DELETED"

class BookDiscount(Base):
    discount_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(BigInteger, ForeignKey("book.book_id"), nullable=False)
    
    discount_rate = Column(Integer, nullable=False)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    
    status = Column(Enum(BookDiscountStatus), default=BookDiscountStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        CheckConstraint('discount_rate BETWEEN 0 AND 100', name='check_book_discount_rate_range'),
    )
