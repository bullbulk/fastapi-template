from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


# noinspection PyUnusedLocal
@router.get("/", response_model=list[schemas.User])
def read_users(
        db: Session = Depends(deps.get_db),
        *,
        current_user: models.User = Depends(deps.get_current_active_superuser),  # Necessary for credentials validation
        offset: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve users. Only for superusers.
    """
    users = crud.user.get_multi(db, offset=offset, limit=limit)
    return users


# noinspection PyUnusedLocal
@router.post("/", response_model=schemas.User)
def create_user(
        db: Session = Depends(deps.get_db),
        *,
        current_user: models.User = Depends(deps.get_current_active_superuser),  # Necessary for credentials validation
        user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user. Only for superusers.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
        db: Session = Depends(deps.get_db),
        *,
        current_user: models.User = Depends(deps.get_current_active_user),
        password: str = Body(None),
        full_name: str = Body(None),
        email: EmailStr = Body(None),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
        *,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schemas.User)
def create_user_open(
        db: Session = Depends(deps.get_db),
        *,
        password: str = Body(...),
        email: EmailStr = Body(...),
        full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
        db: Session = Depends(deps.get_db),
        *,
        current_user: models.User = Depends(deps.get_current_active_user),
        user_id: int,
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return user


# noinspection PyUnusedLocal
@router.put("/{user_id}", response_model=schemas.User)
def update_user(
        db: Session = Depends(deps.get_db),
        *,
        current_user: models.User = Depends(deps.get_current_active_superuser),  # Necessary for credentials validation
        user_id: int,
        user_in: schemas.UserUpdate,
) -> Any:
    """
    Update a user. Only for superusers.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
