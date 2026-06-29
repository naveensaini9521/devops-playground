from sqlalchemy.orm import Session

from app.models import User
from app.security import hash_password
from app.security import verify_password
from app.security import create_access_token


class AuthService:

    @staticmethod
    def register(db: Session, request):

        user = User(
            username=request.username,
            email=request.email,
            password_hash=hash_password(request.password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def login(db: Session, request):

        user = db.query(User).filter(
            User.email == request.email
        ).first()

        if not user:
            return None

        if not verify_password(
                request.password,
                user.password_hash
        ):
            return None

        token = create_access_token(user)

        return token