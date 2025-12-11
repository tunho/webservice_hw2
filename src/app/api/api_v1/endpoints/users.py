from typing import Any, List
from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.db.session import get_db
from app.models.user import User, UserRole, UserStatus
from app.schemas.user import UserCreate, UserUpdate, UserResponse

router = APIRouter()

from app.schemas.common import PageResponse
import math

@router.get("/", response_model=PageResponse[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 20,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users with pagination.
    """
    query = db.query(User)
    total_elements = query.count()
    total_pages = math.ceil(total_elements / size)
    
    users = query.offset(page * size).limit(size).all()
    
    return {
        "content": users,
        "page": page,
        "size": size,
        "totalElements": total_elements,
        "totalPages": total_pages
    }

@router.post("/", response_model=UserResponse)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    # Use dict() to preserve datetime objects for SQLAlchemy
    obj_in_data = user_in.dict()
    del obj_in_data["password"]
    db_obj = User(**obj_in_data, password=security.get_password_hash(user_in.password))
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.put("/me", response_model=UserResponse)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user.
    """
    user_data = jsonable_encoder(current_user)
    update_data = user_in.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["password"] = security.get_password_hash(update_data["password"])
        
    for field in user_data:
        if field in update_data:
            setattr(current_user, field, update_data[field])
            
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if user == current_user:
        return user
    if not deps.get_current_active_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user_by_admin(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update any user (Admin only).
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user_data = jsonable_encoder(user)
    update_data = user_in.dict(exclude_unset=True)
    
    if "password" in update_data and update_data["password"]:
        update_data["password"] = security.get_password_hash(update_data["password"])
        
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])
            
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/logout", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "Successfully logged out"}}}}})
def logout(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Logout (Client should discard token).
    """
    return {"message": "Successfully logged out"}

@router.patch("/me", response_model=UserResponse)
def update_user_me_patch(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user (PATCH).
    """
    user_data = jsonable_encoder(current_user)
    update_data = user_in.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["password"] = security.get_password_hash(update_data["password"])
        
    for field in user_data:
        if field in update_data:
            setattr(current_user, field, update_data[field])
            
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me/soft", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "User soft deleted successfully"}}}}})
def soft_delete_user_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Soft delete own user.
    """
    current_user.status = UserStatus.INACTIVE # Or DELETED if available
    current_user.deleted_at = datetime.now()
    db.add(current_user)
    db.commit()
    return {"message": "User soft deleted successfully"}

@router.delete("/me/hard", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "User permanently deleted"}}}}})
def hard_delete_user_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Hard delete own user.
    """
    db.delete(current_user)
    db.commit()
    return {"message": "User permanently deleted"}
