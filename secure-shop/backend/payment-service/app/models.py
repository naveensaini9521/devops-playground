from sqlalchemy import BigInteger, Column, DateTime, Float, String, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(BigInteger,primary_key=True,autoincrement=True,index=True)

    order_number = Column(String(50),nullable=False,index=True)

    customer_id = Column(BigInteger,nullable=False,index=True)

    amount = Column(Float,nullable=False)

    transaction_id = Column(String(100),unique=True,nullable=False,index=True)

    payment_status = Column(String(30),nullable=False,default="PENDING")

    payment_method = Column(String(50),nullable=True)

    created_at = Column(DateTime(timezone=True),server_default=func.now())

    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

    def __repr__(self):
        return (
            f"<Payment("
            f"order='{self.order_number}', "
            f"amount={self.amount}, "
            f"status='{self.payment_status}')>"
        )