import json
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import (
    PaymentProcessRequest,
    PaymentResponse,
    PaymentDBResponse,
    PaymentRequest
)
from app.services.payment_service import PaymentService
from app.hmac_util import verify_payment_request

router = APIRouter(
    prefix="/payment",
    tags=["Payment"]
)


@router.post("/process", response_model=PaymentResponse)
async def process_payment(
    request: PaymentProcessRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    try:
        result = PaymentService.process_payment(
            db=db,
            request=request
        )
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment processing failed: {str(e)}"
        )


@router.get("/{transaction_id}", response_model=PaymentDBResponse)
def get_payment(
    transaction_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    payment = PaymentService.get_payment_by_transaction_id(
        db=db,
        transaction_id=transaction_id
    )
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    return payment


@router.get("/order/{order_number}", response_model=List[PaymentDBResponse])
def get_payments_by_order(
    order_number: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
 
    payments = PaymentService.get_payments_by_order(
        db=db,
        order_number=order_number
    )
    return payments


@router.get("/", response_model=List[PaymentDBResponse])
def get_all_payments(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    payments = PaymentService.get_all_payments(db)
    return payments

@router.post("/webhook/order-update")
async def order_update_webhook(
    request: Request,
    db: Session = Depends(get_db)
):

    try:
        headers = dict(request.headers)
        
        body_bytes = await request.body()
        body_str = body_bytes.decode('utf-8')
        
        if not verify_payment_request(
            method="POST",
            path="/payment/webhook/order-update",
            headers=headers,
            body=body_str
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid HMAC signature"
            )
        
        data = json.loads(body_str)
        transaction_id = data.get("transaction_id")
        payment_status = data.get("payment_status")
        
        if not transaction_id or not payment_status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields: transaction_id, payment_status"
            )
        
        payment = PaymentService.get_payment_by_transaction_id(
            db=db,
            transaction_id=transaction_id
        )
        
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        
        payment.payment_status = payment_status
        payment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(payment)
        
        return {
            "status": "success",
            "message": "Payment status updated",
            "payment": payment
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )