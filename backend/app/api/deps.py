from __future__ import annotations

from datetime import datetime, timezone
from typing import Generator
from uuid import UUID

from fastapi import Depends, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.errors import ApiError
from app.models.session import UserSession
from app.models.user import User


def get_db(request: Request) -> Generator[Session, None, None]:
    sessionmaker = request.app.state.db_sessionmaker
    db = sessionmaker()
    try:
        yield db
    finally:
        db.close()


def get_current_session(request: Request, db: Session = Depends(get_db)) -> UserSession:
    settings = request.app.state.settings
    raw_session_id = request.cookies.get(settings.session_cookie_name)
    if not raw_session_id:
        raise ApiError(status_code=401, code="not_authenticated", message="Not logged in")

    try:
        session_id = UUID(raw_session_id)
    except ValueError:
        raise ApiError(status_code=401, code="not_authenticated", message="Not logged in")

    user_session = db.scalar(select(UserSession).where(UserSession.id == session_id))
    if user_session is None:
        raise ApiError(status_code=401, code="not_authenticated", message="Not logged in")

    now = datetime.now(timezone.utc)
    if user_session.expires_at <= now:
        db.delete(user_session)
        db.commit()
        raise ApiError(status_code=401, code="not_authenticated", message="Not logged in")

    return user_session


def get_current_user(
    db: Session = Depends(get_db),
    user_session: UserSession = Depends(get_current_session),
) -> User:
    user = db.scalar(select(User).where(User.id == user_session.user_id))
    if user is None:
        db.delete(user_session)
        db.commit()
        raise ApiError(status_code=401, code="not_authenticated", message="Not logged in")

    return user
