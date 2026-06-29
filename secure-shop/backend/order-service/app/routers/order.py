from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import CreateOrderRequest
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

        return OrderService.create_order(
            db=db,
            request=request,
            current_user=current_user
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
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

    order = OrderService.get_order_by_id(
        db,
        order_id
    )

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order