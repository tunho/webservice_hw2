from sqlalchemy import Integer, Column, Integer, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class OrderItem(Base):
    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(BigInteger, ForeignKey("order.order_id"), nullable=False)
    book_id = Column(BigInteger, ForeignKey("book.book_id"), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)
    discount_rate = Column(Integer, default=0)
    subtotal = Column(Integer, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    order = relationship("Order", backref="items")
    book = relationship("Book")
