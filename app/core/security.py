from datetime import datetime, timedelta
from typing import Any

import jwt
from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
        subject: str | Any,
        expires_delta: timedelta = None,
        extra_payload: dict | None = None
) -> str:
    if extra_payload is None:
        extra_payload = {}
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {"exp": expire, "sub": str(subject), "grant_type": "access", **extra_payload}
    encoded_jwt = jwt_encode(payload)
    return encoded_jwt


def create_refresh_token(
        subject: str | Any,
        expires_delta: timedelta = None,
        extra_payload: dict | None = None
) -> str:
    if extra_payload is None:
        extra_payload = {}
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    payload = {"exp": expire, "sub": str(subject), "grant_type": "refresh", **extra_payload}
    encoded_jwt = jwt_encode(payload)
    return encoded_jwt


def write_new_refresh_session(
        db: Session = Depends(deps.get_db),
        *,
        refresh_token,
        user_id,
        fingerprint,
        refresh_expire_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
) -> None:
    refresh_session = schemas.RefreshSessionCreate(
        refresh_token=refresh_token,
        expires_delta=refresh_expire_delta,
        user_id=user_id,
        fingerprint=fingerprint
    )
    crud.refresh_session.create(
        db, obj_in=refresh_session
    )


def create_jwt_pair(
        subject: str | Any,
        fingerprint: str
) -> dict[str, str]:
    access_expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(subject, access_expires_delta),
        "refresh_token": create_refresh_token(subject, refresh_expires_delta, {"fingerprint": fingerprint})
    }


def jwt_encode(payload: dict) -> str:
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def jwt_decode(subject: str) -> dict[str, Any]:
    return jwt.decode(subject, settings.SECRET_KEY, algorithms=[ALGORITHM])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
