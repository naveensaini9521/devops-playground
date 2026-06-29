from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.sql import func

from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    order_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    customer_id = Column(
        BigInteger,
        nullable=False,
        index=True
    )

    customer_name = Column(
        String(100),
        nullable=False
    )

    total_amount = Column(
        Float,
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False,
        default="PENDING"
    )

    transaction_id = Column(
        String(100),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return (
            f"<Order("
            f"order_number='{self.order_number}', "
            f"customer='{self.customer_name}', "
            f"amount={self.total_amount}, "
            f"status='{self.status}')>"
        )