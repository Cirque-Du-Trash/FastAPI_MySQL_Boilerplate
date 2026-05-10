import models
from database import engine
from fastapi import FastAPI
from routers import items

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)


@app.get("/")
def health_check():
    return {"status": "OK", "message": "Server is running!"}
