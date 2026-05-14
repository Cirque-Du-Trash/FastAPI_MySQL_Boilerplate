from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from dependencies import get_current_user

router = APIRouter(prefix="/items", tags=["items"])


@router.post(
    "/", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED
)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_item = models.Item(**item.model_dump(), owner_id=current_user.id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get("/", response_model=list[schemas.ItemResponse])
def read_items(
    skip: int = Query(0, ge=0, le=100),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return db.query(models.Item).offset(skip).limit(limit).all()


@router.get("/me", response_model=list[schemas.ItemResponse])
def read_my_items(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Item).filter(models.Item.owner_id == current_user.id).all()


@router.get("/{item_id}", response_model=schemas.ItemResponse)
def read_item(
    item_id: int = Path(ge=1, le=2147483647),
    db: Session = Depends(get_db),
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int = Path(ge=1, le=2147483647),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not your item"
        )
    db.delete(item)
    db.commit()
