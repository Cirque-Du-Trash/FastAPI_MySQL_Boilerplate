from fastapi import FastAPI

import models
from database import engine
from routers import items

models.Base.metadata.create_all(bind=engine)  # 엔진 연결 및 DB 초기화

app = FastAPI()  # FastAPI 선언

app.include_router(items.router)  # items.py 라우터 분리


@app.get("/")  # 루트 경로 및 헬스 체크
def health_check():
    return {"status": "OK", "message": "Server is running!"}
