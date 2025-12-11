from sqlalchemy import Integer, Column, String, Text, ForeignKey, DateTime, BigInteger
from sqlalchemy.sql import func
from app.db.base_class import Base

class Log(Base):
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=True)
    
    action = Column(String(100), nullable=False)
    detail = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
