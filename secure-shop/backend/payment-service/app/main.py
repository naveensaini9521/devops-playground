from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import json
import hmac
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Payment Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HMAC Secret (must be same as order service)
HMAC_SECRET = os.getenv("HMAC_SECRET", "my-super-secret-hmac-key")

def generate_signature(method: str, path: str, timestamp: str, body: str) -> str:
    """Generate HMAC signature"""
    message = "\n".join([method.upper(), path, timestamp, body])
    signature = hmac.new(
        HMAC_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    return signature

def verify_signature(method: str, path: str, timestamp: str, body: str, received_signature: str) -> bool:
    """Verify HMAC signature"""
    expected_signature = generate_signature(method, path, timestamp, body)
    return hmac.compare_digest(expected_signature, received_signature)

@app.post("/payment/process")
async def process_payment(
    request: Request,
    x_timestamp: str = Header(...),
    x_signature: str = Header(...),
):
    # 1. Get request body
    body_bytes = await request.body()
    body_str = body_bytes.decode('utf-8')
    
    # 2. Log for debugging
    print(f"Received payment request:")
    print(f"Timestamp: {x_timestamp}")
    print(f"Signature: {x_signature}")
    print(f"Body: {body_str}")
    
    # 3. Verify HMAC signature
    is_valid = verify_signature(
        method="POST",
        path="/payment/process",
        timestamp=x_timestamp,
        body=body_str,
        received_signature=x_signature
    )
    
    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid HMAC signature"
        )
    
    # 4. Parse payment data
    payment_data = json.loads(body_str)
    
    # 5. Process payment (mock)
    transaction_id = f"TXN-{payment_data['order_number']}"
    
    # 6. Return response
    return {
        "transaction_id": transaction_id,
        "payment_status": "SUCCESS",
        "order_number": payment_data['order_number'],
        "amount": payment_data['amount']
    }

@app.get("/health")
def health():
    return {"status": "UP"}