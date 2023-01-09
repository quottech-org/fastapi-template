from enum import Enum
from datetime import datetime
import os
from typing import List
from uuid import UUID

import yaml
import aiofiles
from pydantic import BaseModel

class EnvirometTypes(str, Enum):
    test = "test"
    dev = "dev"
    prod = "prod"


def get_conf_path():
    return os.getenv("CONF_PATH", "/Users/q0tik/Projects/UB-back-fastapi/config/config.dev.yml")


class Profile(BaseModel):
  title: str
  description: str
  version: str


class Postgresql(BaseModel):
    host: str
    port: str
    user: str
    password: str
    db_name: str

    @property
    def uri(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    @property
    def uri_postgresql(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}"


class JWT(BaseModel):
    secret: UUID
    access_expiration_time: int
    refresh_expiration_time: int


class AppConfig(BaseModel):
    enviroment: EnvirometTypes
    profile: Profile
    postgres: Postgresql
    jwt: JWT

    @classmethod
    async def from_yaml_file(cls, config_path: str) -> "AppConfig":
        async with aiofiles.open(config_path, mode="r") as f:
            contents = await f.read()
            return cls.parse_obj(yaml.full_load(contents))

    @classmethod
    def from_yaml_file_sync(cls, config_path: str) -> "AppConfig":
        # _start_time = datetime.now()
        with open(config_path, mode="r") as f:
            contents = f.read()
            app_config = cls.parse_obj(yaml.full_load(contents))
            # logger.info(f"Config was parsed successfuly. Processed time: {datetime.now() - _start_time}")
            return app_config
        


app_config = AppConfig.from_yaml_file_sync(get_conf_path())
