from sqlalchemy import Integer, Column, Integer, ForeignKey, BigInteger, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class SettlementItem(Base):
    settlement_item_id = Column(Integer, primary_key=True, autoincrement=True)
    settlement_id = Column(BigInteger, ForeignKey("settlement.settlement_id"), nullable=False)
    order_item_id = Column(BigInteger, ForeignKey("order_item.order_item_id"), nullable=False)
    order_id = Column(BigInteger, ForeignKey("order.order_id"), nullable=False)
    book_id = Column(BigInteger, ForeignKey("book.book_id"), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    item_amount = Column(Integer, nullable=False)
    
    settlement = relationship("Settlement", backref="items")
    
    __table_args__ = (
        CheckConstraint('quantity >= 1', name='check_settlement_quantity_positive'),
        CheckConstraint('item_amount >= 0', name='check_settlement_amount_positive'),
    )
