from pydantic_settings import BaseSettings
import os
class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Project Health Reporting Agent"
    API_V1_STR: str = "/api/v1"
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")

    class Config:
        env_file = ".env"

settings = Settings()

