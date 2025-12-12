from sqlalchemy import Integer, Column, Integer, String, ForeignKey, DateTime, Enum, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class OrderStatus(str, enum.Enum):
    CREATED = "CREATED"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

class PaymentMethod(str, enum.Enum):
    CARD = "CARD"
    ACCOUNT = "ACCOUNT"
    POINT = "POINT"

class Order(Base):
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    
    total_price = Column(Integer, nullable=False)
    discount_amount = Column(Integer, default=0)
    final_price = Column(Integer, nullable=False)
    
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    
    receiver_name = Column(String(100), nullable=False)
    receiver_phone = Column(String(20), nullable=False)
    shipping_address = Column(String(255), nullable=False)
    
    status = Column(Enum(OrderStatus), default=OrderStatus.CREATED, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    paid_at = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    user = relationship("User", backref="orders")
