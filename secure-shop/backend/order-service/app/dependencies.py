from fastapi import Header
from fastapi import HTTPException
from fastapi import status

from app.security import verify_token


def get_current_user(
    authorization: str = Header(...)
):

    if not authorization.startswith("Bearer "):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization Header"
        )

    token = authorization.split(" ")[1]

    payload = verify_token(token)

    return payload