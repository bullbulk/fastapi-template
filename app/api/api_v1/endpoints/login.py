from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app import models
from app import schemas
from app.api import deps
from app.core import security
from app.core.security import write_new_refresh_session, PasswordRequestForm, SessionRequestForm

router = APIRouter()


@router.post("/", response_model=schemas.TokenPair)
def login(
        db: Session = Depends(deps.get_db), form_data: PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests and refresh token for updating it
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    tokens = security.create_jwt_pair(user.id)
    refresh_session = crud.refresh_session.get_active(db, user_id=user.id, fingerprint=form_data.fingerprint)
    if not refresh_session:  # if session with same user_id and fingerprint exists, return it
        write_new_refresh_session(tokens["refresh_token"], user.id, form_data.fingerprint)
    else:
        tokens["refresh_token"] = refresh_session.refresh_token
    return tokens


@router.post("/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/update-token", response_model=schemas.TokenPair)
def update_token(
        db: Session = Depends(deps.get_db),
        session_form: SessionRequestForm = Depends()
) -> Any:
    """
    Token refresh, get a new access token for future requests and refresh token for updating it
    """
    current_session = crud.refresh_session.get_by_token(db, token=session_form.refresh_token)
    if not current_session:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = current_session.user
    crud.refresh_session.remove(db, id=current_session.id)
    if current_session.fingerprint != session_form.fingerprint:  # somebody stole token, we won't send him new pair
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    tokens = security.create_jwt_pair(user.id)
    write_new_refresh_session(tokens["refresh_token"], user.id, current_session.fingerprint)
    return tokens
