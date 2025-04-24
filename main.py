from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app_initializer.app_initializer import AppInitializer
from database_settings import engine
from logger.logger import logger, logging_middleware
from models.entities import Base
from routers import (
    auth_router,
    item_category_router,
    role_router,
    stock_item_router,
    user_router,
)

app = FastAPI()
logger.info("Starting application...")

# Add middlewares
app.middleware("http")(logging_middleware)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app_initializer = AppInitializer()
app_initializer.initialize()

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(stock_item_router.router)
main_router.include_router(item_category_router.router)
main_router.include_router(user_router.router)
main_router.include_router(role_router.router)
main_router.include_router(auth_router.router)

app.include_router(main_router)


@app.get("/")
async def root():
    return {"message": "App is running"}
