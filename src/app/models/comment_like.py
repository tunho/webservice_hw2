from sqlalchemy import Integer, Column, ForeignKey, DateTime, BigInteger, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base_class import Base

class CommentLike(Base):
    like_id = Column(Integer, primary_key=True, autoincrement=True)
    comment_id = Column(BigInteger, ForeignKey("comment.comment_id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        UniqueConstraint('comment_id', 'user_id', name='uq_comment_like_user'),
    )
