from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"]
)

security = HTTPBearer(
    auto_error=False
)


def hash_password(password: str):

    return pwd_context.hash(password)


def verify_password(password, hashed):

    return pwd_context.verify(
        password,
        hashed
    )


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    if credentials is None:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("user_id")

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not user:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return user

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )