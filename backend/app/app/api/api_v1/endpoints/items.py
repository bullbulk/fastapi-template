from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Item])
def read_items(
        db: Session = Depends(deps.get_db),
        *,
        current_user: models.User = Depends(deps.get_current_active_user),
        offset: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve items.
    """
    if crud.user.is_superuser(current_user):
        items = crud.item.get_multi(db, offset=offset, limit=limit)
    else:
        items = crud.item.get_multi_by_owner(
            db=db, owner_id=current_user.id, offset=offset, limit=limit
        )
    return items


@router.post("/", response_model=schemas.Item)
def create_item(
        db: Session = Depends(deps.get_db),
        *,
        current_user: models.User = Depends(deps.get_current_active_user),
        item_in: schemas.ItemCreate,
) -> Any:
    """
    Create new item.
    """
    item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return item


# noinspection PyShadowingBuiltins
@router.put("/{id}", response_model=schemas.Item)
def update_item(
        db: Session = Depends(deps.get_db),
        *,
        current_user: models.User = Depends(deps.get_current_active_user),
        id: int,
        item_in: schemas.ItemUpdate,
) -> Any:
    """
    Update an item.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


# noinspection PyShadowingBuiltins
@router.get("/{id}", response_model=schemas.Item)
def read_item(
        db: Session = Depends(deps.get_db),
        *,
        current_user: models.User = Depends(deps.get_current_active_user),
        id: int,
) -> Any:
    """
    Get item by ID.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return item


# noinspection PyShadowingBuiltins
@router.delete("/{id}", response_model=schemas.Item)
def delete_item(
        db: Session = Depends(deps.get_db),
        *,
        current_user: models.User = Depends(deps.get_current_active_user),
        id: int,
) -> Any:
    """
    Delete an item.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    item = crud.item.remove(db=db, id=id)
    return item
