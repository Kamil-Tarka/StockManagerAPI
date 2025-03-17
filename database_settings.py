from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app_settings import AppSettings

app_settings = AppSettings()

if app_settings.envirnoment == "development":
    db_name = app_settings.db_name
    SQLALCHEMY_DATABASE_URL = f"sqlite:///./{db_name}"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
elif app_settings.envirnoment == "production":
    db_host = app_settings.db_host
    db_user = app_settings.db_user
    db_password = app_settings.db_password
    db_name = app_settings.db_name
    charset = app_settings.charset
    SQLALCHEMY_DATABASE_URL = f"mariadb+pymysql://{db_user}:{db_password}@{db_host}/{db_name}?charset={charset}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
