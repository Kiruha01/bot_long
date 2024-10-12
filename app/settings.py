from typing import Optional

from aiogram.types import BufferedInputFile
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    EMAIL: str
    PASSWORD: str

    TELEGRAM_TOKEN: str
    BASE_URL: AnyHttpUrl
    CERT_PATH: Optional[str] = None

    def get_cert_file(self) -> Optional[BufferedInputFile]:
        if self.CERT_PATH is None:
            return None

        return BufferedInputFile.from_file(self.CERT_PATH)


settings = Settings()  # type: ignore
