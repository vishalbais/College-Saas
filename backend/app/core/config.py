import os
from pydantic import BaseSettings, Field, AnyUrl

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REDIS_URL: str = Field(..., env="REDIS_URL")
    SMTP_HOST: str = Field(None, env="SMTP_HOST")
    SMTP_PORT: int = Field(587, env="SMTP_PORT")
    SMTP_USER: str = Field(None, env="SMTP_USER")
    SMTP_PASSWORD: str = Field(None, env="SMTP_PASSWORD")
    MEDIA_ROOT: str = Field("/data/media", env="MEDIA_ROOT")
    GS_SERVICE_ACCOUNT_JSON: str = Field(None, env="GS_SERVICE_ACCOUNT_JSON")
    FRONTEND_URL: str = Field("http://localhost:5173", env="FRONTEND_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
