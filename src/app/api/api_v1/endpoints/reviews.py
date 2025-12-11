from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.models.review import Review
from app.models.book import Book
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse

router = APIRouter()

@router.post("/{book_id}", response_model=ReviewResponse)
def create_review(
    *,
    db: Session = Depends(get_db),
    book_id: int,
    review_in: ReviewCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new review.
    """
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    review = Review(
        user_id=current_user.user_id,
        book_id=book_id,
        rating=review_in.rating,
        content=review_in.content
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

from app.schemas.common import PageResponse
import math

@router.get("/{book_id}", response_model=PageResponse[ReviewResponse])
def read_reviews(
    book_id: int,
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 20,
) -> Any:
    """
    Get reviews for a book with pagination.
    """
    query = db.query(Review).filter(Review.book_id == book_id)
    total_elements = query.count()
    total_pages = math.ceil(total_elements / size)
    
    reviews = query.offset(page * size).limit(size).all()
    
    return {
        "content": reviews,
        "page": page,
        "size": size,
        "totalElements": total_elements,
        "totalPages": total_pages
    }

@router.patch("/{review_id}")
def update_review(
    review_id: int,
    review_in: ReviewCreate, # Reusing Create schema for simplicity, or create Update schema
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a review.
    """
    review = db.query(Review).filter(Review.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    review.rating = review_in.rating
    review.content = review_in.content
    db.commit()
    db.refresh(review)
    
    return {
        "isSuccess": True,
        "message": "리뷰를 수정했습니다.",
        "payload": {
            "reviewId": review.review_id,
            "updatedAt": review.updated_at
        }
    }

@router.get("/{review_id}/detail", response_model=ReviewResponse)
def read_review(
    review_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Get single review.
    """
    review = db.query(Review).filter(Review.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.delete("/{review_id}", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "Review deleted successfully"}}}}})
def delete_review(
    *,
    db: Session = Depends(get_db),
    review_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete review.
    """
    review = db.query(Review).filter(Review.review_id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != current_user.user_id and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}
