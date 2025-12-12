from sqlalchemy import Integer, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    content = Column(Text, nullable=False)
    view_count = Column(Integer, default=0)
    
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", backref="posts")
    category = relationship("Category", backref="posts")
