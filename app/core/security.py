from datetime import datetime, timedelta
from typing import Any, Optional
from typing import Union, Dict

import jwt
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app import crud, schemas
from app.core.config import settings
from app.db.session import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {"exp": expire, "sub": str(subject), "grant_type": "access"}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    payload = {"exp": expire, "sub": str(subject), "grant_type": "refresh"}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def write_new_refresh_session(
        refresh_token,
        user_id,
        fingerprint,
        refresh_expire_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
):
    db = SessionLocal()
    refresh_session = schemas.RefreshSessionCreate()
    refresh_session.refresh_token = refresh_token
    refresh_session.expires_delta = refresh_expire_delta
    refresh_session.user_id = user_id
    refresh_session.fingerprint = fingerprint
    crud.refresh_session.create(
        db, obj_in=refresh_session
    )
    db.close()


def create_jwt_pair(
        subject: Union[str, Any]
) -> Dict[str, str]:
    access_expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(subject, access_expires_delta),
        "refresh_token": create_refresh_token(subject, refresh_expires_delta)
    }


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(self, grant_type: str = Form(None, regex="password"), username: str = Form(...),
                 password: str = Form(...), fingerprint: str = Form(...), scope: str = Form(""),
                 client_id: Optional[str] = Form(None),
                 client_secret: Optional[str] = Form(None)):
        super().__init__(grant_type, username, password, scope, client_id, client_secret)
        self.fingerprint = fingerprint


class SessionRequestForm:
    def __init__(self, refresh_token: str = Form(...), fingerprint: str = Form(...)):
        self.fingerprint = fingerprint
        self.refresh_token = refresh_token
