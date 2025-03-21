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
        elif self._envirnoment == "development":
            load_dotenv(".envdev")
            self._db_host = os.getenv("DEV_DB_HOST")
            self._db_user = os.getenv("DEV_DB_USER")
            self._db_password = os.getenv("DEV_DB_PASSWORD")
            self._db_name = os.getenv("DEV_DB_NAME")
            self._charset = os.getenv("DEV_CHARSET")
            self._secret_key = os.getenv("DEV_SECRET_KEY")
            self._token_expiration_time = int(os.getenv("DEV_TOKEN_EXPIRATION_TIME"))
            self._refresh_token_expiration_time = int(
                os.getenv("DEV_REFRESH_TOKEN_EXPIRATION_TIME")
            )
            self._alghoritm = os.getenv("DEV_ALGORITHM")
        elif self._envirnoment == "production":
            load_dotenv()
            self._db_host = os.getenv("DB_HOST")
            self._db_user = os.getenv("DB_USER")
            self._db_password = os.getenv("DB_PASSWORD")
            self._db_name = os.getenv("DB_NAME")
            self._charset = os.getenv("CHARSET")
            self._secret_key = os.getenv("SECRET_KEY")
            self._token_expiration_time = int(os.getenv("TOKEN_EXPIRATION_TIME"))
            self._refresh_token_expiration_time = int(
                os.getenv("REFRESH_TOKEN_EXPIRATION_TIME")
            )
            self._alghoritm = os.getenv("ALGORITHM")

    @property
    def envirnoment(self):
        return self._envirnoment

    @property
    def secret_key(self):
        if self._secret_key is None:
            raise NoEnvirnomentVariableException(
                "No SECRET_KEY variable found, SECRET_KEY is required variable"
            )

        return self._secret_key

    @property
    def token_expiration_time(self):
        if self._token_expiration_time is None:
            raise NoEnvirnomentVariableException(
                "No TOKEN_EXPIRATION_TIME variable found, TOKEN_EXPIRATION_TIME  is required variable"
            )

        return self._token_expiration_time

    @property
    def refresh_token_expiration_time(self):
        if self._refresh_token_expiration_time is None:
            raise NoEnvirnomentVariableException(
                "No REFRESH_TOKEN_EXPIRATION_TIME variable found, REFRESH_TOKEN_EXPIRATION_TIME is required variable"
            )

        return self._refresh_token_expiration_time

    @property
    def token_algorithm(self):
        if self._alghoritm is None:
            raise NoEnvirnomentVariableException(
                "No ALGORITHM variable found, ALGORITHM is required variable"
            )

        return self._alghoritm

    @property
    def db_name(self):
        if self._db_name is None:
            raise NoEnvirnomentVariableException(
                "No DB_NAME variable found, DB_NAME is required variable"
            )
        return self._db_name

    @property
    def db_host(self):
        if self._db_host is None:
            raise NoEnvirnomentVariableException(
                "No DB_HOST variable found, DB_HOST is required variable"
            )

        return self._db_host

    @property
    def db_user(self):
        if self._db_user is None:
            raise NoEnvirnomentVariableException(
                "No DB_USER variable found, DB_USER is required variable"
            )

        return self._db_user

    @property
    def db_password(self):
        if self._db_password is None:
            raise NoEnvirnomentVariableException(
                "No DB_PASSWORD variable found, DB_PASSWORD is required variable"
            )

        return self._db_password

    @property
    def charset(self):
        if self._charset is None:
            raise NoEnvirnomentVariableException(
                "No CHARSET variable found, CHARSET is required variable"
            )

        return self._charset
