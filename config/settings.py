import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DUCKDUCKGO_MAX_RESULTS: int = 5
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
