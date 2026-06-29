from fastapi import Header, HTTPException
from typing import Optional
from app.security import verify_token

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization Header"
        )

    try:
        token = authorization.split(" ")[1]
        payload = verify_token(token)
        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )