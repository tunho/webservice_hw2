from typing import Any, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.models.favorite import Favorite
from app.models.book import Book
from app.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteResponse

router = APIRouter()

@router.post("/", response_model=FavoriteResponse)
def create_favorite(
    *,
    db: Session = Depends(get_db),
    favorite_in: FavoriteCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Add book to favorites.
    """
    book = db.query(Book).filter(Book.book_id == favorite_in.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
        
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.user_id,
        Favorite.book_id == favorite_in.book_id
    ).first()
    
    if favorite:
        if not favorite.is_active:
            favorite.is_active = True
            favorite.deleted_at = None
            db.add(favorite)
            db.commit()
            db.refresh(favorite)
        return favorite
        
    favorite = Favorite(
        user_id=current_user.user_id,
        book_id=favorite_in.book_id,
        is_active=True
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

from app.schemas.common import PageResponse
import math

@router.get("/", response_model=PageResponse[FavoriteResponse])
def read_favorites(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 20,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    List active favorites with pagination.
    """
    query = db.query(Favorite).filter(
        Favorite.user_id == current_user.user_id,
        Favorite.is_active == True
    )
    total_elements = query.count()
    total_pages = math.ceil(total_elements / size)
    
    favorites = query.offset(page * size).limit(size).all()
    # Ensure book data is loaded
    for fav in favorites:
        _ = fav.book
    
    return {
        "content": favorites,
        "page": page,
        "size": size,
        "totalElements": total_elements,
        "totalPages": total_pages
    }

@router.delete("/{book_id}", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "Favorite removed successfully"}}}}})
def delete_favorite(
    *,
    db: Session = Depends(get_db),
    book_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Remove book from favorites (Soft Delete).
    """
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.user_id,
        Favorite.book_id == book_id
    ).first()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
        
    favorite.is_active = False
    favorite.deleted_at = datetime.now()
    db.add(favorite)
    db.commit()
    return {"message": "Favorite removed (soft deleted)"}
