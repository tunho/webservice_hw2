from sqlalchemy import Integer, Column, Integer, String, DateTime, Enum, BigInteger, CheckConstraint
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class CouponStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    DISABLED = "DISABLED"

class Coupon(Base):
    coupon_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    
    discount_rate = Column(Integer, nullable=False)
    min_order = Column(Integer, default=0)
    max_discount = Column(Integer, default=0)
    
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    status = Column(Enum(CouponStatus), default=CouponStatus.ACTIVE, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    __table_args__ = (
        CheckConstraint('discount_rate BETWEEN 1 AND 100', name='check_discount_rate_range'),
        CheckConstraint('min_order >= 0', name='check_min_order_positive'),
        CheckConstraint('max_discount >= 0', name='check_max_discount_positive'),
    )
