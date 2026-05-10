from pydantic import BaseModel, ConfigDict


class ItemCreate(
    BaseModel
):  # 서버 -> DB (데이터 생성용) id가 필요 없음, id는 models에서 autoincrement.
    name: str
    price: int


class ItemResponse(BaseModel):  # DB -> 서버 (데이터 응답용) id가 필요함.
    id: int
    name: str
    price: int

    model_config = ConfigDict(
        from_attributes=True
    )  # Pydantic은 기본적으로 딕셔너리만 읽을 수 있음.
    # 하지만 우리가 생성하는 객체(Object)는 SQLAlchemy 모델의 인스턴스이므로 이를 읽을 수 있도록
    # from_attributes=True 옵션을 추가하여 .을 찍어 db_item.name의 형식으로 가져올 수 있도록 하는 설정.
