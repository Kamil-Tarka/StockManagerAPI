import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

if os.getenv("envirnoment") == "development":
    load_dotenv(".envdev")
    db_name = os.getenv("DEV_DB_NAME")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///./{db_name}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
elif os.getenv("envirnoment") == "production":
    load_dotenv()
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    charset = os.getenv("CHARSET")
    SQLALCHEMY_DATABASE_URL = f"mariadb+pymysql://{db_user}:{db_password}@{db_host}/{db_name}?charset={charset}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
