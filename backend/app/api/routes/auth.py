from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_session, get_db
from app.core.errors import ApiError
from app.core.security import hash_password, verify_password
from app.models.session import UserSession
from app.models.user import User
from app.schemas.auth import LoginIn, RegisterIn
from app.schemas.user import UserOut


router = APIRouter(prefix="/auth", tags=["auth"])


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def _set_session_cookie(response: Response, request: Request, session_id: uuid.UUID) -> None:
    settings = request.app.state.settings
    response.set_cookie(
        key=settings.session_cookie_name,
        value=str(session_id),
        max_age=60 * 60 * 24 * settings.session_ttl_days,
        httponly=True,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        path=settings.cookie_path,
    )


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register(payload: RegisterIn, request: Request, response: Response, db: Session = Depends(get_db)):
    settings = request.app.state.settings
    email = _normalize_email(payload.email)

    existing = db.scalar(select(User).where(User.email == email))
    if existing is not None:
        raise ApiError(status_code=409, code="email_taken", message="Email already exists")

    now = datetime.now(timezone.utc)
    user_id = uuid.uuid4()
    session_id = uuid.uuid4()

    user = User(id=user_id, email=email, password_hash=hash_password(payload.password))
    user_session = UserSession(
        id=session_id,
        user_id=user_id,
        expires_at=now + timedelta(days=settings.session_ttl_days),
    )

    db.add(user)
    db.add(user_session)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ApiError(status_code=409, code="email_taken", message="Email already exists")

    db.refresh(user)
    _set_session_cookie(response, request, session_id)
    return user


@router.post(
    "/login",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
)
def login(payload: LoginIn, request: Request, response: Response, db: Session = Depends(get_db)):
    settings = request.app.state.settings
    email = _normalize_email(payload.email)

    user = db.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise ApiError(status_code=401, code="invalid_credentials", message="Invalid credentials")

    now = datetime.now(timezone.utc)
    session_id = uuid.uuid4()
    user_session = UserSession(
        id=session_id,
        user_id=user.id,
        expires_at=now + timedelta(days=settings.session_ttl_days),
    )
    db.add(user_session)
    db.commit()

    _set_session_cookie(response, request, session_id)
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: Request,
    response: Response,
    user_session: UserSession = Depends(get_current_session),
    db: Session = Depends(get_db),
):
    settings = request.app.state.settings
    db.delete(user_session)
    db.commit()

    response.delete_cookie(
        key=settings.session_cookie_name,
        path=settings.cookie_path,
        samesite=settings.cookie_samesite,
        secure=settings.cookie_secure,
        httponly=True,
    )
    response.status_code = status.HTTP_204_NO_CONTENT
    return response
