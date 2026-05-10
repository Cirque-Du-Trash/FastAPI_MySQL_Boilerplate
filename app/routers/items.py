import models
import schemas
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[schemas.ItemResponse])
def read_items(
    skip: int = 0, limit: int = 10, min_price: int = 0, db: Session = Depends(get_db)
):
    items = (
        db.query(models.Item)
        .filter(models.Item.price >= min_price)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return items


@router.get("/{item_id}", response_model=schemas.ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="item not found.")
    return db_item


@router.post("/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(name=item.name, price=item.price)

    db.add(db_item)

    db.commit()

    db.refresh(db_item)

    return db_item
