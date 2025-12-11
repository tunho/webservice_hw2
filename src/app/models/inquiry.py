from sqlalchemy import Integer, Column, String, Text, ForeignKey, DateTime, Enum, BigInteger
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class InquiryStatus(str, enum.Enum):
    PENDING = "PENDING"
    ANSWERED = "ANSWERED"
    CLOSED = "CLOSED"

class Inquiry(Base):
    inquiry_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    
    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    
    status = Column(Enum(InquiryStatus), default=InquiryStatus.PENDING, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    answered_at = Column(DateTime, nullable=True)
