import uuid
import httpx
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models import Payment
from app.schemas import PaymentProcessRequest, PaymentResponse
from app.hmac_util import generate_signature, current_timestamp


class PaymentService:
    """Payment service business logic."""
    
    ORDER_SERVICE_URL = "http://localhost:8002"
    HMAC_SECRET = "094ca51cd6b677d5d34a3aed960821a88f9bb88e93af887eebe6655d9849a69a"
    
    @staticmethod
    def process_payment(
        db: Session,
        request: PaymentProcessRequest
    ) -> PaymentResponse:
        
        transaction_id = "TXN-" + str(uuid.uuid4()).split("-")[0].upper()
        
        payment_status = "COMPLETED"  
        
        payment = Payment(
            order_number=request.order_number,
            customer_id=request.customer_id,
            amount=request.amount,
            transaction_id=transaction_id,
            payment_status=payment_status,
            payment_method=request.payment_method or "CARD"
        )
        
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        PaymentService._update_order_status(
            order_number=request.order_number,
            status=payment_status,
            transaction_id=transaction_id
        )
        
        return PaymentResponse(
            transaction_id=transaction_id,
            order_number=request.order_number,
            amount=request.amount,
            payment_status=payment_status,
            message=f"Payment {payment_status.lower()}"
        )
    
    @staticmethod
    def _update_order_status(
        order_number: str,
        status: str,
        transaction_id: str
    ):

        try:
            payload = {
                "order_number": order_number,
                "status": status,
                "transaction_id": transaction_id
            }
            
            import json
            body = json.dumps(payload, separators=(",", ":"))
            timestamp = current_timestamp()
            
            signature = generate_signature(
                method="POST",
                path="/webhook/payment-callback",
                timestamp=timestamp,
                body=body
            )
            
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    f"{PaymentService.ORDER_SERVICE_URL}/webhook/payment-callback",
                    json=payload,
                    headers={
                        "X-Timestamp": timestamp,
                        "X-Signature": signature,
                        "Content-Type": "application/json"
                    }
                )
                
                if response.status_code != 200:
                    print(f"Failed to update order: {response.text}")
                    
        except Exception as e:
            print(f"Error updating order status: {str(e)}")
    
    @staticmethod
    def get_payment_by_transaction_id(
        db: Session,
        transaction_id: str
    ) -> Optional[Payment]:
        """Get payment by transaction ID."""
        return db.query(Payment).filter(
            Payment.transaction_id == transaction_id
        ).first()
    
    @staticmethod
    def get_payments_by_order(
        db: Session,
        order_number: str
    ):

        return db.query(Payment).filter(
            Payment.order_number == order_number
        ).all()
    
    @staticmethod
    def get_all_payments(db: Session):

        return db.query(Payment).all()