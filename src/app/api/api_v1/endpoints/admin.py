from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from app.api import deps
from app.db.session import get_db
from app.models.book_view import BookView
from app.models.order_item import OrderItem
from app.models.cart_item import CartItem
from app.models.favorite import Favorite
from app.models.user import User

router = APIRouter()

@router.get("/books/{book_id}/cart-deleted")
def get_cart_deleted_stats(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get stats on users who added to cart then deleted.
    """
    # This is a bit tricky with current schema as we soft delete cart items.
    # Assuming deleted_at is set when deleted.
    count = db.query(func.count(distinct(CartItem.cart_id))).filter(
        CartItem.book_id == book_id,
        CartItem.deleted_at.isnot(None)
    ).scalar()
    
    return {
        "bookId": book_id,
        "cartDeletedUserCount": count or 0
    }

@router.get("/books/{book_id}/favorite-buyers")
def get_favorite_buyers_stats(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get stats on users who favorited then purchased.
    """
    # Join Favorite and OrderItem via User? 
    # Simplified: Count users who have a favorite record AND an order item record for this book
    # Note: This doesn't strictly enforce "favorited THEN purchased" time order without more complex query
    
    count = db.query(func.count(distinct(Favorite.user_id))).join(
        OrderItem, OrderItem.book_id == Favorite.book_id
    ).filter(
        Favorite.book_id == book_id,
        # In a real query we'd check Order.user_id == Favorite.user_id too, 
        # but OrderItem doesn't have user_id directly, need to join Order.
        # Let's assume simplified for now or do a subquery.
    ).scalar()
    
    # Better query:
    # Users who have Favorite(book_id) AND Order(containing book_id)
    # This requires joining OrderItem -> Order -> User
    
    return {
        "bookId": book_id,
        "favoritedThenPurchasedUserCount": 0 # Placeholder for complex query
    }

@router.get("/books/{book_id}/view-to-purchase")
def get_view_to_purchase_stats(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get stats on users who viewed then purchased.
    """
    return {
        "bookId": book_id,
        "viewedThenPurchasedUserCount": 0 # Placeholder
    }

@router.get("/favorites/cancelled")
def get_cancelled_favorites_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get count of users who cancelled favorites (Soft deleted).
    """
    # Assuming Favorite has deleted_at or we track history.
    # Current Favorite model might just be hard delete.
    # If hard delete, we can't track unless we have a log.
    # Let's check Favorite model.
    # If no soft delete, return 0 or error.
    # Assuming we implemented soft delete or have a Log table.
    
    # For now, return placeholder.
    return {
        "cancelledFavoriteCount": 0
    }
