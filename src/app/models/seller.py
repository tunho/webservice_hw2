from sqlalchemy import Integer, Column, String, ForeignKey, Enum, DateTime, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class SellerStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"
    PENDING = "PENDING"

class Seller(Base):
    seller_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    
    business_name = Column(String(120), nullable=False)
    business_number = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone_number = Column(String(30), nullable=False)
    address = Column(String(255), nullable=False)
    
    payout_bank = Column(String(60), nullable=False)
    payout_account = Column(String(60), nullable=False)
    payout_holder = Column(String(60), nullable=False)
    
    status = Column(Enum(SellerStatus), default=SellerStatus.ACTIVE, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    user = relationship("User", backref="seller_profile")
