from sqlalchemy import Integer, Column, Integer, Text, ForeignKey, DateTime, BigInteger, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Comment(Base):
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(BigInteger, ForeignKey("review.review_id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    
    content = Column(Text, nullable=False)
    like_count = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    review = relationship("Review", backref="comments")
    user = relationship("User", backref="review_comments")
    
    __table_args__ = (
        CheckConstraint('like_count >= 0', name='check_comment_like_count_positive'),
    )
