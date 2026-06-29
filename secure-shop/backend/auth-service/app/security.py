from pathlib import Path
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


BASE_DIR = Path(__file__).resolve().parent.parent

PRIVATE_KEY = (BASE_DIR / "keys" / "private.pem").read_text()
PUBLIC_KEY = (BASE_DIR / "keys" / "public.pem").read_text()

ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user):

    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    return jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm=ALGORITHM
    )


def verify_token(token: str):

    return jwt.decode(
        token,
        PUBLIC_KEY,
        algorithms=[ALGORITHM]
    )