from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.api import deps
from app.db.session import get_db
from app.models.book import Book, BookStatus
from app.models.user import User, UserRole
from app.models.seller import Seller
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from datetime import datetime

router = APIRouter()

from app.schemas.common import PageResponse
import math

@router.get("/", response_model=PageResponse[BookResponse])
def read_books(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 20,
    keyword: Optional[str] = None,
    category: Optional[str] = None,
) -> Any:
    """
    Retrieve books with pagination.
    """
    query = db.query(Book).filter(Book.status == BookStatus.AVAILABLE)
    
    if keyword:
        query = query.filter(or_(Book.title.ilike(f"%{keyword}%"), Book.authors.ilike(f"%{keyword}%")))
    if category:
        query = query.filter(Book.categories.ilike(f"%{category}%"))
        
    total_elements = query.count()
    total_pages = math.ceil(total_elements / size)
    
    books = query.offset(page * size).limit(size).all()
    
    return {
        "content": books,
        "page": page,
        "size": size,
        "totalElements": total_elements,
        "totalPages": total_pages
    }

@router.post("/", response_model=BookResponse)
def create_book(
    *,
    db: Session = Depends(get_db),
    book_in: BookCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new book.
    """
    if current_user.role not in [UserRole.SELLER, UserRole.ADMIN]:
        raise HTTPException(status_code=400, detail="Not enough privileges")
        
    # Check if seller profile exists if role is SELLER
    seller_id = 1 # Default fallback
    
    if current_user.role == UserRole.SELLER:
        seller = db.query(Seller).filter(Seller.user_id == current_user.user_id).first()
        if not seller:
            raise HTTPException(status_code=400, detail="Seller profile not found. Please register as a seller first.")
        seller_id = seller.seller_id
    elif current_user.role == UserRole.ADMIN:
        # For Admin, try to find any active seller to link to (for testing purposes)
        # In a real app, Admin might specify seller_id in request
        seller = db.query(Seller).first()
        if seller:
            seller_id = seller.seller_id
        else:
             # If no seller exists at all, we can't create a book due to FK constraint
             raise HTTPException(status_code=400, detail="No seller exists in the system to link this book to.")

    db_obj = Book(**book_in.dict(), seller_id=seller_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/{book_id}", response_model=BookResponse)
def read_book(
    *,
    db: Session = Depends(get_db),
    book_id: int,
) -> Any:
    """
    Get book by ID.
    """
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.status == BookStatus.DELETED:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    *,
    db: Session = Depends(get_db),
    book_id: int,
    book_in: BookUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a book.
    """
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.status == BookStatus.DELETED:
        raise HTTPException(status_code=404, detail="Book not found")
        
    # Check permission (Seller owns book or Admin)
    if current_user.role == UserRole.USER:
         raise HTTPException(status_code=403, detail="Not authorized")
         
    update_data = book_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)
        
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "Book deleted successfully"}}}}})
def delete_book(
    *,
    db: Session = Depends(get_db),
    book_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a book (Soft delete by default).
    """
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    if current_user.role == UserRole.USER:
         raise HTTPException(status_code=403, detail="Not authorized")
         
    # Soft delete
    book.status = BookStatus.DELETED
    book.deleted_at = datetime.now()
    
    db.add(book)
    db.commit()
    return {"message": "Book deleted successfully"}
