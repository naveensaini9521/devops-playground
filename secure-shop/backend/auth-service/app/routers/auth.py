from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import RegisterRequest, LoginRequest

from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
        request: RegisterRequest,
        db: Session = Depends(get_db)
):

    user = AuthService.register(
        db,
        request
    )

    return {
        "message": "User Registered",
        "id": user.id
    }


@router.post("/login")
def login(
        request: LoginRequest,
        db: Session = Depends(get_db)
):

    token = AuthService.login(
        db,
        request
    )

    if token is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    return {
        "access_token": token,
        "token_type": "Bearer"
    }

@router.get("/profile")
def profile(current_user=Depends(get_current_user)):
    return {
        "message": "Profile fetched successfully",
        "user": current_user
    }