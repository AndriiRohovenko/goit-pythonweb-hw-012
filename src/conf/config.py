from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

APP_ENV = os.getenv("APP_ENV", "dev")
env_file = ".env" if APP_ENV == "prod" else ".env.dev"
load_dotenv(env_file)


class BaseConfig(BaseSettings):
    APP_ENV: str

    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_SECONDS: int

    API_HOST: str
    API_PORT: int
    API_URL: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_FROM: str

    CLOUDINARY_NAME: str
    CLOUDINARY_API_KEY: int
    CLOUDINARY_API_SECRET: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    def db_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class ProdSettings(BaseConfig):
    """Production-specific settings."""

    pass


class DevSettings(ProdSettings):
    model_config = ConfigDict(env_file=".env.dev", env_file_encoding="utf-8")


config = ProdSettings() if os.getenv("APP_ENV") == "prod" else DevSettings()
