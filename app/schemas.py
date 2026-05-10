from pydantic import BaseModel, ConfigDict


class ItemCreate(BaseModel):
    name: str
    price: int


class ItemResponse(BaseModel):
    id: int
    name: str
    price: int

    model_config = ConfigDict(from_attributes=True)
