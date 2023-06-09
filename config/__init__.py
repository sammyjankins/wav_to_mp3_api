import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class CommonSettings(BaseSettings):
    APP_NAME: str = "wav2mp3"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    # HOST: str = '0.0.0.0'
    HOST: str = os.environ.get("API_HOST")
    PORT: int = os.environ.get("API_PORT")


class DatabaseSettings(BaseSettings):
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD")
    SERVICE_NAME: str = os.environ.get("SERVICE_NAME")


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
