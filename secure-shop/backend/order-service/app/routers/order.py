from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Explicit imports
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import CreateOrderRequest, OrderResponse
from app.services.order_service import OrderService

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/")
def create_order(
    request: CreateOrderRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        result = OrderService.create_order(
            db=db,
            request=request,
            current_user=current_user
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/")
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return OrderService.get_orders(db)

@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    order = OrderService.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

@router.put("/{order_number}/status")
def update_order_status(
    order_number: str,
    status: str,
    transaction_id: str = None,
    db: Session = Depends(get_db),
):
    try:
        return OrderService.update_order_status(
            db=db,
            order_number=order_number,
            status=status,
            transaction_id=transaction_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )