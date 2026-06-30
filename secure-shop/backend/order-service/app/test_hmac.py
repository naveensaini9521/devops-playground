import json
import hmac
import hashlib
import time

HMAC_SECRET = "094ca51cd6b677d5d34a3aed960821a88f9bb88e93af887eebe6655d9849a69a"

def generate_correct_signature():
    timestamp = str(int(time.time()))
    
    # This is exactly what your server expects
    payload = {
        "transaction_id": "TXN-3E1EA308",
        "payment_status": "COMPLETED"
    }
    
    # CRITICAL: No spaces in JSON
    body = json.dumps(payload, separators=(",", ":"))
    
    # Create message
    message = "\n".join([
        "POST",
        "/payment/webhook/order-update",
        timestamp,
        body
    ])
    
    # Generate signature
    signature = hmac.new(
        HMAC_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    
    print("=== Correct Values ===")
    print(f"Timestamp: {timestamp}")
    print(f"Body: {body}")
    print(f"Message (with \\n): {repr(message)}")
    print(f"Signature: {signature}")
    print("======================")
    
    return timestamp, body, signature

if __name__ == "__main__":
    generate_correct_signature()