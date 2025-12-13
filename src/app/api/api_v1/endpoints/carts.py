from typing import Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.models.cart import Cart, CartStatus
from app.models.cart_item import CartItem
from app.models.book import Book
from app.models.user import User
from app.schemas.cart import CartResponse, CartItemCreate

router = APIRouter()

@router.get("/", response_model=CartResponse)
def read_cart(
    user_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current active cart.
    """
    target_user_id = current_user.user_id

    cart = db.query(Cart).filter(
        Cart.user_id == target_user_id,
        Cart.status == CartStatus.ACTIVE
    ).first()
    
    if not cart:
        cart = Cart(user_id=target_user_id, status=CartStatus.ACTIVE)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        
    return cart

@router.post("/items", response_model=CartResponse)
def add_item_to_cart(
    *,
    db: Session = Depends(get_db),
    item_in: CartItemCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Add item to cart.
    """
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.user_id,
        Cart.status == CartStatus.ACTIVE
    ).first()
    
    if not cart:
        cart = Cart(user_id=current_user.user_id, status=CartStatus.ACTIVE)
        db.add(cart)
        db.flush()
        
    book = db.query(Book).filter(Book.book_id == item_in.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    # Check if item already exists
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id,
        CartItem.book_id == item_in.book_id
    ).first()
    
    if cart_item:
        cart_item.quantity += item_in.quantity
        cart_item.subtotal = cart_item.quantity * cart_item.unit_price
    else:
        cart_item = CartItem(
            cart_id=cart.cart_id,
            book_id=item_in.book_id,
            quantity=item_in.quantity,
            unit_price=book.price,
            subtotal=book.price * item_in.quantity
        )
        db.add(cart_item)
        
    # Update cart total
    # This is simplified; in real app, we'd recalculate total from all items
    cart.total_amount += (book.price * item_in.quantity)
    
    db.commit()
    db.refresh(cart)
    return cart

@router.put("/items", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"isSuccess": True, "message": "장바구니 항목이 성공적으로 수정되었습니다.", "payload": {"cartId": 1}}}}}})
def update_cart_item(
    *,
    db: Session = Depends(get_db),
    item_in: CartItemCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update cart item quantity.
    """
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.user_id,
        Cart.status == CartStatus.ACTIVE
    ).first()
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
        
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id,
        CartItem.book_id == item_in.book_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not in cart")
        
    cart_item.quantity = item_in.quantity
    # Recalculate subtotal
    cart_item.subtotal = cart_item.quantity * cart_item.unit_price
    
    db.commit()
    
    return {
        "isSuccess": True,
        "message": "장바구니 항목이 성공적으로 수정되었습니다.",
        "payload": {
            "cartId": cart.cart_id
        }
    }

@router.get("/items")
def read_cart_items(
    user_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get cart items.
    """
    target_user_id = current_user.user_id

    cart = db.query(Cart).filter(
        Cart.user_id == target_user_id,
        Cart.status == CartStatus.ACTIVE
    ).first()
    
    items = []
    if cart:
        items = db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).all()
        
    payload = []
    for item in items:
        payload.append({
            "cartItemId": item.cart_item_id,
            "bookId": item.book_id,
            "quantity": item.quantity
        })
        
    return {
        "isSuccess": True,
        "message": "장바구니 항목 목록이 성공적으로 조회되었습니다.",
        "payload": payload
    }

@router.delete("/items/{book_id}", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "Cart item soft deleted"}}}}})
def delete_cart_item(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete item from cart (Soft delete).
    """
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.user_id,
        Cart.status == CartStatus.ACTIVE
    ).first()
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
        
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id,
        CartItem.book_id == book_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not in cart")
        
    # Hard delete from DB or Soft delete?
    # Schema has deleted_at, so soft delete.
    # But for cart items, usually hard delete is fine.
    # Let's do hard delete for simplicity as "Soft Delete" usually implies keeping record.
    # User asked for "DEL 장바구니 도서 항목 소프트 삭제" -> Soft Delete.
    
    cart_item.deleted_at = datetime.now()
    db.add(cart_item)
    db.commit()
    
    return {"message": "Cart item soft deleted"}

@router.delete("/", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "Cart cleared successfully"}}}}})
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Clear all items from the current active cart.
    """
    cart = db.query(Cart).filter(
        Cart.user_id == current_user.user_id,
        Cart.status == CartStatus.ACTIVE
    ).first()
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
        
    # Delete all items in the cart
    db.query(CartItem).filter(CartItem.cart_id == cart.cart_id).delete()
    
    # Reset total amount
    cart.total_amount = 0
    
    db.commit()
    return {"message": "Cart cleared successfully"}
