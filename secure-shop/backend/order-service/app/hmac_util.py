import os
import time
import hmac
import hashlib

from dotenv import load_dotenv

load_dotenv()

HMAC_SECRET = os.getenv("HMAC_SECRET", "my-super-secret-hmac-key")


def generate_signature(method: str,
                       path: str,
                       timestamp: str,
                       body: str) -> str:

    message = "\n".join([
        method.upper(),
        path,
        timestamp,
        body
    ])

    signature = hmac.new(
        HMAC_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return signature


def verify_signature(method: str,
                     path: str,
                     timestamp: str,
                     body: str,
                     received_signature: str) -> bool:

    expected_signature = generate_signature(
        method,
        path,
        timestamp,
        body
    )

    return hmac.compare_digest(
        expected_signature,
        received_signature
    )


def current_timestamp() -> str:
    
    return str(int(time.time()))