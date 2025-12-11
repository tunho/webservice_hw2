from sqlalchemy import Integer, Column, ForeignKey, Boolean, DateTime, BigInteger, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class UserCoupon(Base):
    user_coupon_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    coupon_id = Column(BigInteger, ForeignKey("coupon.coupon_id"), nullable=False)
    
    is_used = Column(Boolean, default=False, nullable=False)
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    user = relationship("User", backref="coupons")
    coupon = relationship("Coupon")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'coupon_id', name='uq_user_coupon'),
    )
