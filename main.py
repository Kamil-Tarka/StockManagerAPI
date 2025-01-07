from fastapi import FastAPI

from database_settings import engine
from models.entities import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}
