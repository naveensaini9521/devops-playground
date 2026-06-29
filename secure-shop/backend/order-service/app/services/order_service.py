import json
import uuid

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
    def create_order(
        db: Session,
        request: CreateOrderRequest,
        current_user: dict
    ):

        total_amount = 0

        order_items = []

        for item in request.items:

            if item.name not in PRODUCTS:
                raise ValueError(
                    f"Product '{item.name}' not found."
                )

            price = PRODUCTS[item.name]

            subtotal = price * item.quantity

            total_amount += subtotal

            order_items.append(
                {
                    "name": item.name,
                    "price": price,
                    "quantity": item.quantity,
                    "subtotal": subtotal
                }
            )

        order_number = (
            "ORD-" +
            str(uuid.uuid4()).split("-")[0].upper()
        )

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

            "amount": total_amount

        }

        body = json.dumps(
            payment_payload,
            separators=(",", ":")
        )

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
    def get_orders(db: Session):

        return db.query(Order).all()

    @staticmethod
    def get_order_by_id(
        db: Session,
        order_id: int
    ):

        return db.query(Order).filter(
            Order.id == order_id
        ).first()