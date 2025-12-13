from typing import Any, List
from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException, Path
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
            status_code=409,
            detail="The user with this email already exists in the system.",
        )
    
    user_phone = db.query(User).filter(User.phone_number == user_in.phone_number).first()
    if user_phone:
        raise HTTPException(
            status_code=409,
            detail="The user with this phone number already exists in the system.",
        )
    
    # Use dict() to preserve datetime objects for SQLAlchemy
    obj_in_data = user_in.dict()
    del obj_in_data["password"]
    db_obj = User(**obj_in_data, password=security.get_password_hash(user_in.password))
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    db.refresh(db_obj)
    return db_obj

@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

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
    user_id: int = Path(..., example=1),
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
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
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



@router.delete("/{user_id}/hard", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "User permanently deleted by admin"}}}}})
def delete_user_by_admin(
    user_id: int = Path(..., example=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Hard delete a user by Admin.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    db.delete(user)
    db.commit()
    return {"message": "User permanently deleted by admin"}
