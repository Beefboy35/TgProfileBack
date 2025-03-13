import os

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    BOT_TOKEN: str
    DB_URL: str = "postgres://postgres:1234@localhost:5432/postgres"
    LOG_FORMAT: str = "{time: YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    FRONT_URL: str
    BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        env_ignore_empty=True,
        extra="ignore",
    )


settings = Setting()
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
logger.add(sink=log_file_path, format=settings.LOG_FORMAT, level="INFO")
database_url = settings.DB_URL