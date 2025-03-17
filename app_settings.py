import os

from dotenv import load_dotenv

from exceptions.exceptions import NoEnvirnomentVariableException


class AppSettings:
    def __init__(self):
        self._envirnoment = os.getenv("envirnoment")
        if self._envirnoment is None:
            raise NoEnvirnomentVariableException(
                "No envirnoment variable found, envirnoment variable is required and must have a value of either 'development', 'test' or 'production'"
            )

    @property
    def envirnoment(self):
        return self._envirnoment

    @property
    def secret_key(self):
        if self._envirnoment == "development":
            load_dotenv(".envdev")
        elif self._envirnoment == "production":
            load_dotenv()

        secret_key = os.getenv("SECRET_KEY")
        if secret_key is None:
            raise NoEnvirnomentVariableException(
                "No SECRET_KEY variable found, SECRET_KEY is required variable"
            )

        return secret_key

    @property
    def token_expiration_time(self):
        if self._envirnoment == "development":
            load_dotenv(".envdev")
        elif self._envirnoment == "production":
            load_dotenv()

        token_expiration_time = os.getenv("TOKEN_EXPIRATION_TIME")
        if token_expiration_time is None:
            raise NoEnvirnomentVariableException(
                "No TOKEN_EXPIRATION_TIME variable found, TOKEN_EXPIRATION_TIME  is required variable"
            )

        return token_expiration_time

    @property
    def token_algorithm(self):
        if self._envirnoment == "development":
            load_dotenv(".envdev")
        elif self._envirnoment == "production":
            load_dotenv()

        alghoritm = os.getenv("ALGORITHM")
        if alghoritm is None:
            raise NoEnvirnomentVariableException(
                "No ALGORITHM variable found, ALGORITHM is required variable"
            )

        return alghoritm

    @property
    def db_name(self):
        if self._envirnoment == "development":
            load_dotenv(".envdev")
        elif self._envirnoment == "production":
            load_dotenv()

        db_name = os.getenv("DB_NAME")
        if db_name is None:
            raise NoEnvirnomentVariableException(
                "No DB_NAME variable found, DB_NAME is required variable"
            )

        return db_name

    @property
    def db_host(self):
        if self._envirnoment == "development":
            load_dotenv(".envdev")
        elif self._envirnoment == "production":
            load_dotenv()

        db_host = os.getenv("DB_HOST")
        if db_host is None:
            raise NoEnvirnomentVariableException(
                "No DB_HOST variable found, DB_HOST is required variable"
            )

        return db_host

    @property
    def db_user(self):
        if self._envirnoment == "development":
            load_dotenv(".envdev")
        elif self._envirnoment == "production":
            load_dotenv()

        db_user = os.getenv("DB_USER")
        if db_user is None:
            raise NoEnvirnomentVariableException(
                "No DB_USER variable found, DB_USER is required variable"
            )

        return db_user

    @property
    def db_password(self):
        if self._envirnoment == "development":
            load_dotenv(".envdev")
        elif self._envirnoment == "production":
            load_dotenv()

        db_password = os.getenv("DB_PASSWORD")
        if db_password is None:
            raise NoEnvirnomentVariableException(
                "No DB_PASSWORD variable found, DB_PASSWORD is required variable"
            )

        return db_password

    @property
    def charset(self):
        if self._envirnoment == "development":
            load_dotenv(".envdev")
        elif self._envirnoment == "production":
            load_dotenv()

        charset = os.getenv("CHARSET")
        if charset is None:
            raise NoEnvirnomentVariableException(
                "No CHARSET variable found, CHARSET is required variable"
            )

        return charset
