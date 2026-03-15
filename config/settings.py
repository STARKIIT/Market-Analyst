import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DUCKDUCKGO_MAX_RESULTS: int = 5
    
    class Config:
        env_file = ".env"

settings = Settings()
