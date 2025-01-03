from fastapi import FastAPI

from database_settings import engine
from models.models import Base, ItemCategory

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    a = ItemCategory()
    return a
