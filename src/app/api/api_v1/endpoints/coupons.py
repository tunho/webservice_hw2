from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.models.coupon import Coupon
from app.models.user import User, UserRole
from app.schemas.coupon import CouponCreate, CouponResponse

router = APIRouter()

@router.post("/", response_model=CouponResponse)
def create_coupon(
    *,
    db: Session = Depends(get_db),
    coupon_in: CouponCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new coupon (Admin only).
    """
    coupon = Coupon(**coupon_in.dict())
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

from app.schemas.common import PageResponse
import math

@router.get("/", response_model=PageResponse[CouponResponse])
def read_coupons(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 20,
) -> Any:
    """
    List active coupons with pagination.
    """
    query = db.query(Coupon)
    total_elements = query.count()
    total_pages = math.ceil(total_elements / size)
    
    coupons = query.offset(page * size).limit(size).all()
    
    return {
        "content": coupons,
        "page": page,
        "size": size,
        "totalElements": total_elements,
        "totalPages": total_pages
    }

@router.patch("/{coupon_id}", response_model=CouponResponse)
def update_coupon(
    *,
    db: Session = Depends(get_db),
    coupon_id: int,
    coupon_in: CouponCreate, # Reusing Create schema
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update coupon (Admin only).
    """
    coupon = db.query(Coupon).filter(Coupon.coupon_id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
        
    update_data = coupon_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(coupon, field, value)
        
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

@router.delete("/{coupon_id}", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "Coupon deleted successfully"}}}}})
def delete_coupon(
    *,
    db: Session = Depends(get_db),
    coupon_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete coupon (Admin only).
    """
    coupon = db.query(Coupon).filter(Coupon.coupon_id == coupon_id).first()
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
        
    db.delete(coupon)
    db.commit()
    return {"message": "Coupon deleted"}
