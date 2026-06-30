from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from app.database import Base, engine
from app.routers.order import router as order_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Order Service",
    description="Secure Order Microservice",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  
        "http://localhost:3000",  
        "http://localhost:8000",  
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,  
)

app.include_router(order_router)

@app.get("/")
def home():
    return {
        "service": "Order Service",
        "status": "Running",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {
        "status": "UP"
    }