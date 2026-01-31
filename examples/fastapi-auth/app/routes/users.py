from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select

from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database import get_session
from app.models import User
from app.mail import send_two_factor_toggled_email

router = APIRouter()
security = HTTPBearer()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")

    user = session.get(User, int(user_id))
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "email_verified": user.email_verified,
        "two_factor_enabled": user.two_factor_enabled,
    }


@router.post("/toggle-2fa")
def toggle_2fa(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    user.two_factor_enabled = not user.two_factor_enabled
    session.add(user)
    session.commit()

    send_two_factor_toggled_email(user.email, user.two_factor_enabled)
    return {
        "two_factor_enabled": user.two_factor_enabled,
        "message": f"2FA {'enabled' if user.two_factor_enabled else 'disabled'}",
    }
