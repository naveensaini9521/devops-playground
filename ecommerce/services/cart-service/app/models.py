from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from shared.database import Base

class Cart(Base):
    __tablename__ = 'carts'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String, default='active')  # active, abandoned, checked_out
    
    items = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__ = 'cart_items'
    
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey('carts.id'))
    product_id = Column(Integer, nullable=False)
    product_name = Column(String)
    quantity = Column(Integer, default=1)
    price = Column(Float)
    
    cart = relationship("Cart", back_populates="items")