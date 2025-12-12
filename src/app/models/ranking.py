from sqlalchemy import Integer, Column, Integer, String, ForeignKey, DateTime, Enum, BigInteger, CheckConstraint
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum

class RankingPeriod(str, enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"

class Ranking(Base):
    ranking_id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("book.book_id"), nullable=False)
    
    ranking_position = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    
    category = Column(String(50), nullable=False)
    age_group = Column(String(20), nullable=True)
    gender = Column(String(10), nullable=True)
    region = Column(String(50), nullable=True)
    
    period_type = Column(Enum(RankingPeriod), default=RankingPeriod.DAILY, nullable=False)
    period_start = Column(DateTime, nullable=True)
    period_end = Column(DateTime, nullable=True)
    
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        CheckConstraint('ranking_position >= 1', name='check_rank_positive'),
        CheckConstraint('score >= 0', name='check_score_positive'),
    )
