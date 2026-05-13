from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    price: int = Field(ge=0, le=2147483647)


class ItemResponse(BaseModel):
    id: int
    name: str = Field
    price: int = Field(ge=0)

    model_config = ConfigDict(from_attributes=True)
