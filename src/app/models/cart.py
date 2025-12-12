from sqlalchemy import Integer, Column, Integer, String, ForeignKey, DateTime, Enum, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class CartStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ORDERED = "ORDERED"
    DELETED = "DELETED"

class Cart(Base):
    cart_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    
    total_amount = Column(Integer, default=0)
    status = Column(Enum(CartStatus), default=CartStatus.ACTIVE, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    user = relationship("User", backref="carts")
