from sqlalchemy import Column, Integer, String, text

from database import Base


class Item(
    Base
):  # database.py의 DeclarativeBase를 상속받음으로써 이 파이썬 클래스는 DB 테이블로 변신함.
    __tablename__ = "items"  # 실제 DB에 생성될 테이블 이름

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(
        Integer, nullable=False, server_default=text("0")
    )  # server_default는 파이썬이 아닌
    # Raw SQL로 DB에 명령을 전달하고 싶을 때, text로 감싸서 이건 RAW SQL이다 라고 알려주는 역할을 함.
