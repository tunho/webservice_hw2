from sqlalchemy import Integer, Column, Integer, Text, ForeignKey, DateTime, Enum, BigInteger, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class ReviewStatus(str, enum.Enum):
    VISIBLE = "VISIBLE"
    HIDDEN = "HIDDEN"
    DELETED = "DELETED"

class Review(Base):
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.book_id"), nullable=False)
    
    rating = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    like_count = Column(Integer, default=0)
    
    status = Column(Enum(ReviewStatus), default=ReviewStatus.VISIBLE, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    user = relationship("User", backref="reviews")
    book = relationship("Book", backref="reviews")
    
    __table_args__ = (
        CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating_range'),
        CheckConstraint('like_count >= 0', name='check_like_count_positive'),
    )
