from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import logging
from datetime import datetime

from shared.database import get_db
from shared.kafka.kafka_client import kafka_client, Event
from shared.redis.redis_client import redis_client
from app.models import Cart, CartItem

app = FastAPI(title="Cart Service", version="1.0.0")

# Pydantic models
class CartItemCreate(BaseModel):
    product_id: int
    product_name: str
    quantity: int = 1
    price: float

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    price: float

class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[CartItemResponse]
    total: float
    status: str

# Business logic functions
def calculate_cart_total(cart: Cart) -> float:
    """Calculate total price of cart"""
    return sum(item.price * item.quantity for item in cart.items)

def get_cached_cart(user_id: int) -> Optional[dict]:
    """Get cart from Redis cache"""
    cache_key = f"cart:user:{user_id}"
    return redis_client.get_json(cache_key)

def cache_cart(user_id: int, cart_data: dict, ttl: int = 1800):
    """Cache cart in Redis with TTL"""
    cache_key = f"cart:user:{user_id}"
    redis_client.set_json(cache_key, cart_data, ttl)

# API endpoints
@app.post("/api/cart/{user_id}/items")
async def add_to_cart(
    user_id: int,
    item: CartItemCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Add item to user's cart"""
    try:
        # Get or create cart
        cart = db.query(Cart).filter(
            Cart.user_id == user_id,
            Cart.status == 'active'
        ).first()
        
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.flush()
        
        # Check if item already exists in cart
        existing_item = db.query(CartItem).filter(
            CartItem.cart_id == cart.id,
            CartItem.product_id == item.product_id
        ).first()
        
        if existing_item:
            existing_item.quantity += item.quantity
        else:
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price
            )
            db.add(cart_item)
        
        db.commit()
        db.refresh(cart)
        
        # Cache the updated cart
        cart_data = {
            'id': cart.id,
            'user_id': cart.user_id,
            'items': [
                {
                    'id': item.id,
                    'product_id': item.product_id,
                    'product_name': item.product_name,
                    'quantity': item.quantity,
                    'price': item.price
                }
                for item in cart.items
            ],
            'total': calculate_cart_total(cart),
            'status': cart.status
        }
        
        # Cache in background
        background_tasks.add_task(cache_cart, user_id, cart_data)
        
        # Publish event
        background_tasks.add_task(
            kafka_client.publish_event,
            Event(
                topic='cart_events',
                event_type='cart.updated',
                data={
                    'user_id': user_id,
                    'cart_id': cart.id,
                    'action': 'add_item',
                    'product_id': item.product_id,
                    'quantity': item.quantity
                }
            )
        )
        
        return {
            'message': 'Item added to cart',
            'cart_id': cart.id,
            'total': calculate_cart_total(cart)
        }
        
    except Exception as e:
        logging.error(f"Error adding to cart: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/cart/{user_id}")
async def get_cart(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get user's cart with caching"""
    # Try cache first
    cached_cart = get_cached_cart(user_id)
    if cached_cart:
        return cached_cart
    
    # Get from database
    cart = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.status == 'active'
    ).first()
    
    if not cart:
        return {'user_id': user_id, 'items': [], 'total': 0, 'status': 'empty'}
    
    cart_data = {
        'id': cart.id,
        'user_id': cart.user_id,
        'items': [
            {
                'id': item.id,
                'product_id': item.product_id,
                'product_name': item.product_name,
                'quantity': item.quantity,
                'price': item.price
            }
            for item in cart.items
        ],
        'total': calculate_cart_total(cart),
        'status': cart.status
    }
    
    # Cache for future requests
    cache_cart(user_id, cart_data)
    
    return cart_data

@app.delete("/api/cart/{user_id}/items/{item_id}")
async def remove_from_cart(
    user_id: int,
    item_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    cart = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.status == 'active'
    ).first()
    
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    
    # Update cache
    background_tasks.add_task(redis_client.delete, f"cart:user:{user_id}")
    
    # Publish event
    background_tasks.add_task(
        kafka_client.publish_event,
        Event(
            topic='cart_events',
            event_type='cart.updated',
            data={
                'user_id': user_id,
                'cart_id': cart.id,
                'action': 'remove_item',
                'item_id': item_id
            }
        )
    )
    
    return {'message': 'Item removed from cart'}