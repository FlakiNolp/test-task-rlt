from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=r'../../.env')
    MONGO_INITDB_ROOT_USERNAME: str = Field(alias='MONGO_INITDB_ROOT_USERNAME')
    MONGO_INITDB_ROOT_PASSWORD: str = Field(alias='MONGO_INITDB_ROOT_PASSWORD')
    ME_CONFIG_MONGODB_SERVER: str = Field(alias='ME_CONFIG_MONGODB_SERVER')
    ME_CONFIG_MONGODB_ADMINUSERNAME: str = Field(alias='ME_CONFIG_MONGODB_ADMINUSERNAME')
    ME_CONFIG_MONGODB_ADMINPASSWORD: str = Field(alias='ME_CONFIG_MONGODB_ADMINPASSWORD')
    ME_CONFIG_MONGODB_PORT: str = Field(alias='ME_CONFIG_MONGODB_PORT')
    ME_CONFIG_BASICAUTH_USERNAME: str = Field(alias='ME_CONFIG_BASICAUTH_USERNAME')
    ME_CONFIG_BASICAUTH_PASSWORD: str = Field(alias='ME_CONFIG_BASICAUTH_PASSWORD')
    TOKEN: str = Field(alias='TOKEN')


config = Config()
