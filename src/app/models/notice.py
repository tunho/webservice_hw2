from sqlalchemy import Integer, Column, String, Text, ForeignKey, DateTime, Enum, BigInteger
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class NoticeStatus(str, enum.Enum):
    VISIBLE = "VISIBLE"
    HIDDEN = "HIDDEN"

class Notice(Base):
    notice_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    
    status = Column(Enum(NoticeStatus), default=NoticeStatus.VISIBLE, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
