from pydantic import (
    BaseSettings,
    PostgresDsn,
    Field,
)

class Settings(BaseSettings):
    database_uri: PostgresDsn = Field(env="DATABASE")
    secret_key: str = Field(env="SECRET_KEY")
    enc_algo: str = Field(env="ALGORITHM")

    class Config:
        env_file = ".env"


config = Settings()
