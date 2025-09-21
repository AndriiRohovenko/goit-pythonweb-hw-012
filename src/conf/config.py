from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

APP_ENV = os.getenv("APP_ENV", "dev")
env_file = ".env" if APP_ENV == "prod" else ".env.dev"
load_dotenv(env_file)


class BaseConfig(BaseSettings):
    # make default values for all vars based on type

    APP_ENV: str = "dev"

    JWT_SECRET: str = "your_jwt_secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_SECONDS: int = 3600

    API_HOST: str = "localhost"
    API_PORT: int = 8005
    API_URL: str = "http://localhost:8005"

    DB_HOST: str = "localhost"
    DB_PORT: int = 4543
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "postgres"

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "your_email@gmail.com"
    SMTP_PASSWORD: str = "your_email_password"
    SMTP_FROM: str = "your_email@gmail.com"

    CLOUDINARY_NAME: str = "your_cloud_name"
    CLOUDINARY_API_KEY: int = 123456789
    CLOUDINARY_API_SECRET: str = "your_api_secret"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    # REDIS_DB: int = 0
    REDIS_PASSWORD: str = "your_redis_password"

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
