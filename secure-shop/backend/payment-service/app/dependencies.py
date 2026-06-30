from fastapi import Header, HTTPException, status
from typing import Optional

from app.security import verify_token


def get_current_user(
    authorization: Optional[str] = Header(None)
):
    """Extract and validate JWT token."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization Header"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization Header"
        )

    token = authorization.split(" ")[1]
    payload = verify_token(token)
    return payload