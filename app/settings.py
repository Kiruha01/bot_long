from typing import Optional

from aiogram.types import BufferedInputFile
from pydantic import AnyHttpUrl, field_validator, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    EMAILS: list[str]
    PASSWORDS: list[str]

    TELEGRAM_TOKEN: str
    BASE_URL: AnyHttpUrl
    CERT_PATH: Optional[str] = None

    # @field_validator("EMAILS", "PASSWORDS", check_fields=False)
    # @classmethod
    # def emails_and_passwords(cls, value: str) -> list[str]:
    #     if value is None:
    #         return value
    #
    #     return value.split(",")

    def get_cert_file(self) -> Optional[BufferedInputFile]:
        if self.CERT_PATH is None:
            return None

        return BufferedInputFile.from_file(self.CERT_PATH)


settings = Settings()  # type: ignore
