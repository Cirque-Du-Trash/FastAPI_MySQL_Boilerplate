from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/items", tags=["items"]
)  # Prefix 설정, /items 경로가 붙은 모든 경로는 이 라우터가 관리함.


@router.get(
    "/", response_model=list[schemas.ItemResponse]
)  # response_model을 지정함으로써 응답의 스키마를 강제하고
def read_items(  # 클라이언트 측에는 필요한 정보만 넘기는 캡슐화의 일종
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
    if db_item is None:  # Guard Clause 패턴
        raise HTTPException(status_code=404, detail="아이템 정보가 없습니다.")
    return db_item


@router.post("/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(name=item.name, price=item.price)

    db.add(db_item)

    db.commit()

    db.refresh(
        db_item
    )  # 오토커밋과 오토플러시를 설정하지 않았기 때문에 수동으로 DB 반영 및 최신 객체를 받아오는 과정.

    return db_item
