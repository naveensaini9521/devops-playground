# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from app.database import Base, engine
from app.routers.payment import router as payment_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Payment Service",
    description="Secure Payment Microservice with HMAC Verification",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8001",
        "http://localhost:8002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(payment_router)


@app.get("/")
def home():
    return {
        "service": "Payment Service",
        "status": "Running",
        "version": "1.0.0",
        "features": [
            "HMAC Signature Verification",
            "Payment Processing",
            "Order Status Updates"
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": "Payment Service"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)