from sqlalchemy import Integer, Column, Integer, ForeignKey, DateTime, Enum, BigInteger, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class SettlementStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELED = "CANCELED"

class Settlement(Base):
    settlement_id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(BigInteger, ForeignKey("seller.seller_id"), nullable=False)
    
    total_sales = Column(Integer, nullable=False)
    commission = Column(Integer, default=0)
    final_payout = Column(Integer, nullable=False)
    
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    status = Column(Enum(SettlementStatus), default=SettlementStatus.PENDING, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    paid_at = Column(DateTime, nullable=True)
    
    seller = relationship("Seller", backref="settlements")
    
    __table_args__ = (
        CheckConstraint('total_sales >= 0', name='check_total_sales_positive'),
        CheckConstraint('commission >= 0', name='check_commission_positive'),
        CheckConstraint('final_payout >= 0', name='check_final_payout_positive'),
    )
