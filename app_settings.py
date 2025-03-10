import os

from dotenv import load_dotenv


class AppSettings:
    def __init__(self):
        self.envirnoment = os.getenv("envirnoment")

    @property
    def secret_key(self):
        if self.envirnoment == "development":
            load_dotenv(".envdev")
        elif self.envirnoment == "production":
            load_dotenv()

        return os.getenv("SECRET_KEY")

    @property
    def token_expiration_time(self):
        if self.envirnoment == "development":
            load_dotenv(".envdev")
        elif self.envirnoment == "production":
            load_dotenv()

        return int(os.getenv("TOKEN_EXPIRATION_TIME"))

    @property
    def token_algorithm(self):
        if self.envirnoment == "development":
            load_dotenv(".envdev")
        elif self.envirnoment == "production":
            load_dotenv()

        return os.getenv("TOKEN_ALGORITHM")
