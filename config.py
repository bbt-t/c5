from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field, SecretStr


class DBConfigENV(BaseSettings):
    host: str = Field(..., env="HOST")
    port: int = Field(..., env="PG_PORT")
    db_name: str = Field(..., env="POSTGRES_DB")
    db_user: str = Field(..., env="POSTGRES_USER")
    password: SecretStr = Field(..., env="POSTGRES_PASSWORD")


class DBConfigFile(BaseSettings):
    host: str
    port: int
    db_name: str
    db_user: str
    password: SecretStr

    class Config:
        case_sentive = False
        env_file = f"{Path(__file__).parent}/.env"
        env_file_encoding = "utf-8"


class PGConfig:
    @staticmethod
    @lru_cache
    def _env():
        return DBConfigENV()

    @staticmethod
    @lru_cache
    def _file():
        return DBConfigFile()

    @property
    def env(self) -> DBConfigENV:
        return self._env()

    @property
    def file(self) -> DBConfigFile:
        return self._file()
