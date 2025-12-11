from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.models.seller import Seller, SellerStatus
from app.models.user import User, UserRole
from app.schemas.seller import SellerCreate, SellerResponse, SellerUpdate

router = APIRouter()

@router.post("/", response_model=SellerResponse)
def register_seller(
    *,
    db: Session = Depends(get_db),
    seller_in: SellerCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Register as a seller.
    """
    if current_user.role != UserRole.USER:
        raise HTTPException(status_code=400, detail="User is already a seller or admin")
        
    seller = Seller(
        user_id=current_user.user_id,
        **seller_in.dict()
    )
    db.add(seller)
    
    # Upgrade user role
    current_user.role = UserRole.SELLER
    db.add(current_user)
    
    db.commit()
    db.refresh(seller)
    return seller

@router.get("/me", response_model=SellerResponse)
def read_seller_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get own seller profile.
    """
    seller = db.query(Seller).filter(Seller.user_id == current_user.user_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller profile not found")
    return seller

@router.patch("/me", response_model=SellerResponse)
def update_seller_me(
    *,
    db: Session = Depends(get_db),
    seller_in: SellerUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update own seller profile.
    """
    seller = db.query(Seller).filter(Seller.user_id == current_user.user_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller profile not found")
        
    update_data = seller_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(seller, field, value)
        
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller

@router.delete("/me/soft", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "Seller profile soft deleted"}}}}})
def soft_delete_seller_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Soft delete own seller profile.
    """
    seller = db.query(Seller).filter(Seller.user_id == current_user.user_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller profile not found")
        
    seller.status = SellerStatus.INACTIVE 
    db.add(seller)
    db.commit()
    return {"message": "Seller profile soft deleted"}

@router.delete("/me/hard", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "Seller profile permanently deleted"}}}}})
def hard_delete_seller_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Hard delete own seller profile.
    """
    seller = db.query(Seller).filter(Seller.user_id == current_user.user_id).first()
    if not seller:
        raise HTTPException(status_code=404, detail="Seller profile not found")
        
    db.delete(seller)
    current_user.role = UserRole.USER
    db.add(current_user)
    
    db.commit()
    return {"message": "Seller profile permanently deleted"}
