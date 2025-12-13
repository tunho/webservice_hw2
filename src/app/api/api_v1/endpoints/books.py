from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.api import deps
from app.db.session import get_db
from app.models.book import Book, BookStatus
from app.models.user import User, UserRole
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
    sort: str = "created_at,desc",
) -> Any:
    """
    Retrieve books with pagination.
    """
    query = db.query(Book).filter(Book.status == BookStatus.AVAILABLE)
    
    if keyword:
        query = query.filter(or_(Book.title.ilike(f"%{keyword}%"), Book.authors.ilike(f"%{keyword}%")))
    if category:
        query = query.filter(Book.categories.ilike(f"%{category}%"))
        
    # Sorting logic
    try:
        sort_field, sort_dir = sort.split(",")
        if sort_dir.lower() == "desc":
            query = query.order_by(getattr(Book, sort_field).desc())
        else:
            query = query.order_by(getattr(Book, sort_field).asc())
    except (ValueError, AttributeError):
        # Fallback to default if invalid sort format or field
        query = query.order_by(Book.created_at.desc())
        
    total_elements = query.count()
    total_pages = math.ceil(total_elements / size)
    
    books = query.offset(page * size).limit(size).all()
    
    return {
        "content": books,
        "page": page,
        "size": size,
        "totalElements": total_elements,
        "totalPages": total_pages,
        "sort": sort
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
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    # Check duplicate ISBN
    existing_book = db.query(Book).filter(Book.isbn == book_in.isbn).first()
    if existing_book:
        raise HTTPException(status_code=409, detail="A book with this ISBN already exists.")
        
    db_obj = Book(**book_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/{book_id}", response_model=BookResponse)
def read_book(
    *,
    db: Session = Depends(get_db),
    book_id: int = Path(..., example=1),
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
    book_id: int = Path(..., example=1),
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
        
    # Check permission (Admin only)
    if current_user.role != UserRole.ADMIN:
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
    book_id: int = Path(..., example=1),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a book (Soft delete by default).
    """
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    if current_user.role != UserRole.ADMIN:
         raise HTTPException(status_code=403, detail="Not authorized")
         
    # Soft delete
    book.status = BookStatus.DELETED
    book.deleted_at = datetime.now()
    
    db.add(book)
    db.commit()
    return {"message": "Book deleted successfully"}
