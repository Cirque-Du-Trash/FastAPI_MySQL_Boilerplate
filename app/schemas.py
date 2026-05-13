from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    price: int = Field(ge=0, le=2147483647)


class ItemResponse(BaseModel):
    id: int
    name: str
    price: int = Field(ge=0)
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str = Field(min_length=6, max_length=25)
    password: str = Field(min_length=6, max_length=25)


class UserResponse(BaseModel):
    id: int
    username: str
    is_superuser: bool

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
