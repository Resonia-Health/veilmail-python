import secrets
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select

from app.database import get_session
from app.models import (
    PasswordResetToken,
    TwoFactorToken,
    User,
    VerificationToken,
)
from app.mail import (
    send_password_changed_email,
    send_password_reset_email,
    send_two_factor_code,
    send_verification_email,
    send_welcome_email,
)
from app.routes.users import create_access_token

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Verify2FARequest(BaseModel):
    email: EmailStr
    password: str
    code: str


class ResetPasswordRequest(BaseModel):
    email: EmailStr


class NewPasswordRequest(BaseModel):
    token: str
    password: str


@router.post("/register")
def register(body: RegisterRequest, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == body.email)).first()
    if existing:
        raise HTTPException(400, "Email already registered")

    user = User(
        name=body.name,
        email=body.email,
        hashed_password=pwd_context.hash(body.password),
    )
    session.add(user)
    session.commit()

    token = VerificationToken(email=body.email)
    session.add(token)
    session.commit()

    send_verification_email(body.email, token.token)
    return {"message": "Verification email sent"}


@router.get("/verify-email")
def verify_email(token: str, session: Session = Depends(get_session)):
    record = session.exec(
        select(VerificationToken).where(VerificationToken.token == token)
    ).first()

    if not record:
        raise HTTPException(400, "Invalid token")
    if record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(400, "Token expired")

    user = session.exec(select(User).where(User.email == record.email)).first()
    if not user:
        raise HTTPException(404, "User not found")

    user.email_verified = True
    session.delete(record)
    session.commit()

    send_welcome_email(user.email, user.name)
    return {"message": "Email verified"}


@router.post("/login")
def login(body: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == body.email)).first()
    if not user or not pwd_context.verify(body.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    if not user.email_verified:
        token = VerificationToken(email=body.email)
        session.add(token)
        session.commit()
        send_verification_email(body.email, token.token)
        raise HTTPException(403, "Email not verified. Verification email resent.")

    if user.two_factor_enabled:
        code = f"{secrets.randbelow(900000) + 100000}"
        tf_token = TwoFactorToken(email=body.email, code=code)
        session.add(tf_token)
        session.commit()
        send_two_factor_code(body.email, code)
        return {"two_factor_required": True}

    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify-2fa")
def verify_2fa(body: Verify2FARequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == body.email)).first()
    if not user or not pwd_context.verify(body.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    record = session.exec(
        select(TwoFactorToken).where(
            TwoFactorToken.email == body.email, TwoFactorToken.code == body.code
        )
    ).first()

    if not record:
        raise HTTPException(400, "Invalid code")
    if record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(400, "Code expired")

    session.delete(record)
    session.commit()

    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot-password")
def forgot_password(body: ResetPasswordRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == body.email)).first()
    if user:
        token = PasswordResetToken(email=body.email)
        session.add(token)
        session.commit()
        send_password_reset_email(body.email, token.token)

    return {"message": "If an account exists, a reset email has been sent"}


@router.post("/reset-password")
def reset_password(body: NewPasswordRequest, session: Session = Depends(get_session)):
    record = session.exec(
        select(PasswordResetToken).where(PasswordResetToken.token == body.token)
    ).first()

    if not record:
        raise HTTPException(400, "Invalid token")
    if record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(400, "Token expired")

    user = session.exec(select(User).where(User.email == record.email)).first()
    if not user:
        raise HTTPException(404, "User not found")

    user.hashed_password = pwd_context.hash(body.password)
    session.delete(record)
    session.commit()

    send_password_changed_email(user.email)
    return {"message": "Password updated"}
