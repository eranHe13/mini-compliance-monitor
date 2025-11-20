from pydantic_settings import BaseSettings 
import os
class Settings(BaseSettings):
    DB_URL: str = os.getenv("DB_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()