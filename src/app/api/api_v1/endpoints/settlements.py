from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.db.session import get_db
from app.models.settlement import Settlement, SettlementStatus
from app.models.seller import Seller
from app.models.user import User, UserRole
from app.schemas.settlement import SettlementCreate, SettlementUpdate, SettlementResponse

router = APIRouter()

@router.post("/", response_model=SettlementResponse)
def create_settlement(
    *,
    db: Session = Depends(get_db),
    settlement_in: SettlementCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Request settlement (Seller only).
    """
    seller = db.query(Seller).filter(Seller.user_id == current_user.user_id).first()
    
    # Allow Admin to create settlement for testing (pick first seller)
    if not seller and current_user.role == UserRole.ADMIN:
        seller = db.query(Seller).first()

    if not seller:
        raise HTTPException(status_code=404, detail="Seller profile not found")
        
    # Simplified: Create settlement record. In real app, calculate amount from orders.
    settlement = Settlement(
        seller_id=seller.seller_id,
        period_start=settlement_in.period_start,
        period_end=settlement_in.period_end,
        total_sales=0, # Placeholder
        commission=0,
        final_payout=0,
        status=SettlementStatus.PENDING
    )
    db.add(settlement)
    db.commit()
    db.refresh(settlement)
    return settlement

from app.schemas.common import PageResponse
import math

@router.get("/", response_model=PageResponse[SettlementResponse])
def read_settlements(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 20,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    List settlements (Seller sees own, Admin sees all) with pagination.
    """
    if current_user.role == UserRole.ADMIN:
        query = db.query(Settlement)
    else:
        seller = db.query(Seller).filter(Seller.user_id == current_user.user_id).first()
        if not seller:
             # Return empty page
             return {
                 "content": [],
                 "page": page,
                 "size": size,
                 "totalElements": 0,
                 "totalPages": 0
             }
        query = db.query(Settlement).filter(Settlement.seller_id == seller.seller_id)
        
    total_elements = query.count()
    total_pages = math.ceil(total_elements / size)
    
    settlements = query.offset(page * size).limit(size).all()
        
    return {
        "content": settlements,
        "page": page,
        "size": size,
        "totalElements": total_elements,
        "totalPages": total_pages
    }

@router.patch("/{settlement_id}", response_model=SettlementResponse)
def update_settlement(
    *,
    db: Session = Depends(get_db),
    settlement_id: int,
    settlement_in: SettlementUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update settlement status (Admin only).
    """
    settlement = db.query(Settlement).filter(Settlement.settlement_id == settlement_id).first()
    if not settlement:
        raise HTTPException(status_code=404, detail="Settlement not found")
        
    if settlement_in.status:
        settlement.status = settlement_in.status
        
    db.add(settlement)
    db.commit()
    db.refresh(settlement)
    return settlement

@router.delete("/{settlement_id}", responses={200: {"description": "Successful Response", "content": {"application/json": {"example": {"message": "Settlement deleted"}}}}})
def delete_settlement(
    *,
    db: Session = Depends(get_db),
    settlement_id: int,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete settlement (Admin only).
    """
    settlement = db.query(Settlement).filter(Settlement.settlement_id == settlement_id).first()
    if not settlement:
        raise HTTPException(status_code=404, detail="Settlement not found")
        
    db.delete(settlement)
    db.commit()
    return {"message": "Settlement deleted"}
