from sqlalchemy import Integer, Column, ForeignKey, DateTime, BigInteger
from sqlalchemy.sql import func
from app.db.base_class import Base

class BookView(Base):
    view_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=True)
    book_id = Column(Integer, ForeignKey("book.book_id"), nullable=False)
    
    viewed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
