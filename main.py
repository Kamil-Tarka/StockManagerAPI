from fastapi import APIRouter, FastAPI

from database_settings import engine
from models.entities import Base
from routers import item_category_router, role_router, stock_item_router, user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(stock_item_router.router)
main_router.include_router(item_category_router.router)
main_router.include_router(user_router.router)
main_router.include_router(role_router.router)

app.include_router(main_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
