# from typing import Literal
# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

#     DB_HOST: str
#     DB_PORT: int
#     DB_USER: str
#     DB_PASS: str
#     DB_NAME: str

#     REDIS_HOST: str
#     REDIS_PORT: str

#     @property
#     def REDIS_URL(self):
#         return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

#     @property
#     def DB_URL(self):
#         return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

#     JWT_SECRET_KEY: str
#     JWT_ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int
#     model_config = SettingsConfigDict(env_file=".env")


# settings = Settings()

import os
import sys
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


def _is_pytest_process() -> bool:
    if os.getenv("PYTEST_CURRENT_TEST") or os.getenv("PYTEST_VERSION"):
        return True
    return any("pytest" in arg for arg in sys.argv)


class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: str

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(env_file=".env-test" if _is_pytest_process() else ".env")


settings = Settings()