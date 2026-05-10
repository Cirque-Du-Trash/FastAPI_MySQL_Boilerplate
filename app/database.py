import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()  # dotenv는 .env 파일을 탐색하고 그 내용을 읽은 다음 OS의 환경변수 메모리에 주입하는 역할을 함.

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DB_URL"
)  # 파이썬의 기본 내장함수인 os.getenv는 그 환경변수 메모리를 읽어옴.

if not SQLALCHEMY_DATABASE_URL:  # 환경 변수 설정 체크
    raise ValueError("DB_URL 환경 변수가 설정되지 않았습니다.")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)  # 엔진은 기본적으로 파이썬과 DB 사이의 통신 케이블이며, 기본 설정이 저장되어 있음. 하지만 인자를 통해 커스터마이징이 가능함.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,  # SessionLocal은 싱글톤 패턴을 적용하여 매번 get_db() 호출 시 리소스를 아낄 수 있음
)  # 세션은 쿼리가 실행되는 창구, 세션메이커는 세션을 생성하는 공장
# autocommit=False: 오토 커밋 관련 인자, 기본값은 거짓이나 명시적으로 표기하기 위함
# autoflush=False, 쿼리를 날리기 전에 메모리 상의 값과 실제 DB 간의 Diff를 비교해서 플러싱 후 쿼리를 실행하는 기능,
# 기본값은 참이며, 이 기능은 성능 저하 및 데드락을 방지하고, 의도한 시점에 쿼리를 실행하기 위해 거짓으로 설정.
# 엔진과 바인딩하는 이유는 세션이 쿼리를 어디에 날려야할 지 기본값이 설정되지 않았기 때문.
Base = (
    declarative_base()
)  # Base는 메타데이터를 저장하는 객체로서, 파이썬은 DB 테이블 구조인지 일반 클래스인지 알 수 없기 때문에 명시적으로 선언한다는 의미.


def get_db():  # 제너레이터 함수
    db = SessionLocal()  # 위에서 생성한 싱글톤 SessionLocal을 호출하여 세션 생성
    try:
        yield db  # 일시정지
    finally:
        db.close()  # 작업이 성공하든, 오류가 발생하든 일단 DB와의 연결을 끊음.
