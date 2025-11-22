from pydantic_settings import BaseSettings 
import os
class Settings(BaseSettings):
    DB_URL: str = os.getenv("DB_URL")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()