from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.models.book_discount import BookDiscount, BookDiscountStatus
from app.models.book import Book
from app.models.user import User, UserRole
from app.schemas.discount import DiscountCreate, DiscountUpdate, DiscountResponse

router = APIRouter()

@router.post("/", response_model=DiscountResponse)
def create_discount(
    *,
    db: Session = Depends(get_db),
    discount_in: DiscountCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create a book discount (Seller/Admin).
    """
    if current_user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    book = db.query(Book).filter(Book.book_id == discount_in.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    discount = BookDiscount(**discount_in.dict())
    db.add(discount)
    db.commit()
    db.refresh(discount)
    return discount

from app.schemas.common import PageResponse
import math

@router.get("/", response_model=PageResponse[DiscountResponse])
def read_discounts(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 20,
) -> Any:
    """
    List discounts with pagination.
    """
    query = db.query(BookDiscount)
    total_elements = query.count()
    total_pages = math.ceil(total_elements / size)
    
    discounts = query.offset(page * size).limit(size).all()
    
    return {
        "content": discounts,
        "page": page,
        "size": size,
        "totalElements": total_elements,
        "totalPages": total_pages
    }

@router.patch("/{discount_id}", response_model=DiscountResponse)
def update_discount(
    *,
    db: Session = Depends(get_db),
    discount_id: int,
    discount_in: DiscountUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update discount.
    """
    if current_user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    discount = db.query(BookDiscount).filter(BookDiscount.discount_id == discount_id).first()
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
        
    update_data = discount_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(discount, field, value)
        
    db.add(discount)
    db.commit()
    db.refresh(discount)
    return discount

@router.delete("/{discount_id}", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "Discount deleted successfully"}}}}})
def delete_discount(
    *,
    db: Session = Depends(get_db),
    discount_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete discount (Soft delete).
    """
    if current_user.role == UserRole.USER:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    discount = db.query(BookDiscount).filter(BookDiscount.discount_id == discount_id).first()
    if not discount:
        raise HTTPException(status_code=404, detail="Discount not found")
        
    discount.status = BookDiscountStatus.EXPIRED # Or DELETED
    db.add(discount)
    db.commit()
    return {"message": "Discount deleted"}
