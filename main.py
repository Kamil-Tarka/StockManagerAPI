from fastapi import FastAPI

from database_settings import engine
from models.entities import Base
from routers import stock_item_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(stock_item_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
