import json
import uuid
from datetime import datetime
from typing import List, Dict, Any

from sqlalchemy.orm import Session

from app.models import Order
from app.schemas import CreateOrderRequest, OrderItem
from app.hmac_util import generate_signature, current_timestamp


PRODUCTS = {
    "T-Shirt": 799,
    "Pajama": 999,
    "Jeans": 1999,
    "Hoodie": 2499,
    "Jacket": 3999,
    "Shoes": 3499,
    "Track Pant": 1499,
    "Cap": 499,
    "Shorts": 899,
    "Sweater": 2299
}


class OrderService:

    @staticmethod
    def create_order(
        db: Session,
        request: CreateOrderRequest,
        current_user: dict
    ) -> Dict[str, Any]:

        total_amount = 0
        order_items = []

        for item in request.items:
            if item.name not in PRODUCTS:
                raise ValueError(
                    f"Product '{item.name}' not found in catalog."
                )

            price = PRODUCTS[item.name]
            subtotal = price * item.quantity
            total_amount += subtotal

            order_items.append({
                "name": item.name,
                "price": price,
                "quantity": item.quantity,
                "subtotal": subtotal
            })

        order_number = "ORD-" + str(uuid.uuid4()).split("-")[0].upper()

        order = Order(
            order_number=order_number,
            customer_id=int(current_user["sub"]),
            customer_name=current_user["username"],
            total_amount=total_amount,
            status="PENDING"
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        payment_payload = {
            "order_number": order.order_number,
            "customer_id": order.customer_id,
            "amount": total_amount,
            "timestamp": current_timestamp()
        }

        body = json.dumps(payment_payload, separators=(",", ":"))

        timestamp = current_timestamp()

        signature = generate_signature(
            method="POST",
            path="/payment/process",
            timestamp=timestamp,
            body=body
        )

        payment_headers = {
            "X-Timestamp": timestamp,
            "X-Signature": signature,
            "Content-Type": "application/json"
        }

        return {
            "message": "Order Created Successfully",
            "order_number": order.order_number,
            "customer": order.customer_name,
            "total_amount": total_amount,
            "status": order.status,
            "items": order_items,
            "payment_request": {
                "headers": payment_headers,
                "body": payment_payload
            }
        }
        
    @staticmethod
    def get_orders(db: Session) -> List[Order]:

        return db.query(Order).all()

    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order:

        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def update_order_status(
        db: Session,
        order_number: str,
        status: str,
        transaction_id: str = None
    ) -> Order:

        order = db.query(Order).filter(
            Order.order_number == order_number
        ).first()
        
        if not order:
            raise ValueError(f"Order {order_number} not found")
        
        order.status = status
        if transaction_id:
            order.transaction_id = transaction_id
        order.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(order)
        
        return order