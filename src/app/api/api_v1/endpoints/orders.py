from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.book import Book
from app.models.user import User, UserRole
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter()

@router.post("/", response_model=OrderResponse)
def create_order(
    *,
    db: Session = Depends(get_db),
    order_in: OrderCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new order.
    """
    # Calculate total price and validate stock
    total_price = 0
    final_price = 0
    
    # Create Order
    db_order = Order(
        user_id=current_user.user_id,
        payment_method=order_in.payment_method,
        receiver_name=order_in.receiver_name,
        receiver_phone=order_in.receiver_phone,
        shipping_address=order_in.shipping_address,
        total_price=0, # Will update
        final_price=0, # Will update
        status=OrderStatus.CREATED
    )
    db.add(db_order)
    db.flush() # Get ID
    
    # Optimized: Fetch all books in one query
    book_ids = [item.book_id for item in order_in.items]
    books = db.query(Book).filter(Book.book_id.in_(book_ids)).all()
    books_map = {b.book_id: b for b in books}

    for item in order_in.items:
        book = books_map.get(item.book_id)
        if not book:
            raise HTTPException(status_code=404, detail=f"Book {item.book_id} not found")
        if book.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for book {book.title}")
            
        # Update stock
        book.stock -= item.quantity
        
        # Create OrderItem
        db_item = OrderItem(
            order_id=db_order.order_id,
            book_id=item.book_id,
            quantity=item.quantity,
            unit_price=book.price,
            subtotal=book.price * item.quantity
        )
        db.add(db_item)
        total_price += db_item.subtotal
        
    db_order.total_price = total_price
    db_order.final_price = total_price # Apply discount logic here if needed
    
    db.commit()
    db.refresh(db_order)
    return db_order

from app.schemas.common import PageResponse
import math

@router.get("/", response_model=PageResponse[OrderResponse])
def read_orders(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 20,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve own orders with pagination. Admin can view all orders.
    """
    if current_user.role == UserRole.ADMIN:
        query = db.query(Order)
    else:
        query = db.query(Order).filter(Order.user_id == current_user.user_id)
    total_elements = query.count()
    total_pages = math.ceil(total_elements / size)
    
    orders = query.offset(page * size).limit(size).all()
    
    return {
        "content": orders,
        "page": page,
        "size": size,
        "totalElements": total_elements,
        "totalPages": total_pages
    }

@router.patch("/{order_id}", response_model=OrderResponse)
def update_order(
    *,
    db: Session = Depends(get_db),
    order_id: int,
    status: OrderStatus = Query(..., description="New status for the order"),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update order status (Cancel, Return, etc).
    """
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    if order.user_id != current_user.user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    order.status = status
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
