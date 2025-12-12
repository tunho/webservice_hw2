from sqlalchemy import Integer, Column, ForeignKey, Boolean, DateTime, BigInteger, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Favorite(Base):
    favorite_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    book_id = Column(Integer, ForeignKey("book.book_id"), nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    user = relationship("User", backref="favorites")
    book = relationship("Book")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'book_id', name='uq_favorite_user_book'),
    )
