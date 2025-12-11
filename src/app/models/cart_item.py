from sqlalchemy import Integer, Column, Integer, ForeignKey, DateTime, BigInteger, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class CartItem(Base):
    cart_item_id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(BigInteger, ForeignKey("cart.cart_id"), nullable=False)
    book_id = Column(BigInteger, ForeignKey("book.book_id"), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)
    discount_rate = Column(Integer, default=0)
    subtotal = Column(Integer, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    cart = relationship("Cart", backref="items")
    book = relationship("Book")
    
    __table_args__ = (
        UniqueConstraint('cart_id', 'book_id', name='uq_cart_item_book'),
    )
