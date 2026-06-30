import os
import time
import hmac
import hashlib

from dotenv import load_dotenv

load_dotenv()

HMAC_SECRET = os.getenv(
    "HMAC_SECRET",
    "094ca51cd6b677d5d34a3aed960821a88f9bb88e93af887eebe6655d9849a69a"
)


def generate_signature(method: str, path: str, timestamp: str, body: str) -> str:
    message = "\n".join([
        method.upper(),
        path,
        timestamp,
        body
    ])

    return hmac.new(
        HMAC_SECRET.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def verify_signature(method: str, path: str, timestamp: str, body: str, signature: str) -> bool:
    expected = generate_signature(method, path, timestamp, body)

    return hmac.compare_digest(expected, signature)


def verify_payment_request(method: str, path: str, headers: dict, body: str) -> bool:
    timestamp = headers.get("x-timestamp")
    signature = headers.get("x-signature")

    if not timestamp or not signature:
        print("Missing HMAC headers")
        return False

    return verify_signature(
        method=method,
        path=path,
        timestamp=timestamp,
        body=body,
        signature=signature
    )


def current_timestamp() -> str:
    return str(int(time.time()))