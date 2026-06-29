import json
import uuid
import httpx
from sqlalchemy.orm import Session
from app.models import Order
from app.schemas import CreateOrderRequest
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
    def create_order(db: Session, request: CreateOrderRequest, current_user: dict):
        # Calculate total and create order
        total_amount = 0
        order_items = []

        for item in request.items:
            if item.name not in PRODUCTS:
                raise ValueError(f"Product '{item.name}' not found.")
            price = PRODUCTS[item.name]
            subtotal = price * item.quantity
            total_amount += subtotal
            order_items.append({
                "name": item.name,
                "price": price,
                "quantity": item.quantity,
                "subtotal": subtotal
            })

        order_number = f"ORD-{str(uuid.uuid4()).split('-')[0].upper()}"
        
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

        # Prepare payment request
        payment_payload = {
            "order_number": order.order_number,
            "customer_id": order.customer_id,
            "amount": total_amount
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

        # ACTUALLY CALL PAYMENT SERVICE
        payment_response = None
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    "http://localhost:8003/payment/process",
                    headers=payment_headers,
                    json=payment_payload
                )
                if response.status_code == 200:
                    payment_response = response.json()
                    # Update order with transaction ID
                    order.transaction_id = payment_response.get("transaction_id")
                    order.status = "PROCESSING"
                    db.commit()
                    db.refresh(order)
                else:
                    print(f"Payment failed: {response.text}")
        except Exception as e:
            print(f"Payment service error: {e}")
            # Order remains PENDING

        return {
            "message": "Order Created Successfully",
            "order_number": order.order_number,
            "customer": order.customer_name,
            "total_amount": total_amount,
            "status": order.status,
            "items": order_items,
            "payment_response": payment_response,
            "payment_request": {
                "headers": payment_headers,
                "body": payment_payload
            }
        }