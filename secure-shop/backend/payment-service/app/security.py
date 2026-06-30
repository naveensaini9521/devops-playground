# app/security.py
import os
from pathlib import Path

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_KEY_PATH = BASE_DIR / "keys" / "public.pem"

try:
    with open(PUBLIC_KEY_PATH, "rb") as f:
        PUBLIC_KEY = f.read()
except FileNotFoundError:
    print(f"Warning: Public key not found at {PUBLIC_KEY_PATH}")
    PUBLIC_KEY = None

ALGORITHM = os.getenv("JWT_ALGORITHM", "RS256")


def verify_token(token: str):
    """Verify JWT token."""
    if not PUBLIC_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Public key not configured"
        )
    
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )