from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api import deps
from app.db.session import get_db
from app.models.book import Book
from app.models.ranking import Ranking, RankingPeriod
from app.models.book_view import BookView
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart_item import CartItem
from app.models.favorite import Favorite
from app.models.user import User

router = APIRouter()

@router.get("/rankings/viewed")
def get_view_rankings(
    db: Session = Depends(get_db),
) -> Any:
    """
    Get book view rankings.
    """
    # Simplified: Just return top viewed books based on BookView count
    # In real app, we would use the Ranking table pre-calculated
    rankings = db.query(
        BookView.book_id, func.count(BookView.view_id).label("score")
    ).group_by(BookView.book_id).order_by(func.count(BookView.view_id).desc()).limit(10).all()
    
    result = []
    for idx, (book_id, score) in enumerate(rankings):
        result.append({
            "rank": idx + 1,
            "score": score,
            "bookId": book_id
        })
        
    return {"books": result}

@router.get("/books/{book_id}/rating")
def get_book_rating(
    book_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get average rating for a book.
    """
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return {
        "bookId": book.book_id,
        "averageRating": float(book.average_rating) if book.average_rating else 0.0,
        "reviewCount": book.review_count
    }

@router.get("/rankings/purchased")
def get_purchase_rankings(
    db: Session = Depends(get_db),
) -> Any:
    """
    Get book purchase rankings.
    """
    # Simplified: Count OrderItems
    rankings = db.query(
        OrderItem.book_id, func.sum(OrderItem.quantity).label("score")
    ).group_by(OrderItem.book_id).order_by(func.sum(OrderItem.quantity).desc()).limit(10).all()
    
    result = []
    for idx, (book_id, score) in enumerate(rankings):
        result.append({
            "rank": idx + 1,
            "score": int(score) if score else 0,
            "bookId": book_id
        })
    return {"books": result}

@router.get("/rankings/demographics/age")
def get_age_rankings(
    db: Session = Depends(get_db),
) -> Any:
    """
    Get rankings by age group (Placeholder).
    """
    return {"message": "Age demographics ranking not implemented yet (requires complex query)"}

@router.get("/rankings/demographics/gender")
def get_gender_rankings(
    db: Session = Depends(get_db),
) -> Any:
    """
    Get rankings by gender (Placeholder).
    """
    return {"message": "Gender demographics ranking not implemented yet"}

@router.get("/rankings/demographics/region")
def get_region_rankings(
    db: Session = Depends(get_db),
) -> Any:
    """
    Get rankings by region (Placeholder).
    """
    return {"message": "Region demographics ranking not implemented yet"}
