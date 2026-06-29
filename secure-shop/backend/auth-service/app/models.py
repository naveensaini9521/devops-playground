from sqlalchemy import Column, String, BigInteger, Boolean
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    username = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    password_hash = Column(String(255), nullable=False)

    role = Column(String(30), default="CUSTOMER")

    is_active = Column(Boolean, default=True)