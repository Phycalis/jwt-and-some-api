from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

load_dotenv()


class AppConfig(BaseSettings):
    API_KEY: str
    BASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1


config = AppConfig()

print(config.API_KEY)
