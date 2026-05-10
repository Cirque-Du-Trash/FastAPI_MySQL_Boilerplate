from database import Base
from sqlalchemy import Column, Integer, String, text


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False, server_default=text("0"))
