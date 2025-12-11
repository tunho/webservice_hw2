from sqlalchemy import Integer, Column, Integer, ForeignKey
from app.db.base_class import Base

class Like(Base):
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True)
