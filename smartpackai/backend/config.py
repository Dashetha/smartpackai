# backend/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    APP_NAME: str = "SmartPack AI"
    API_PREFIX: str = "/api"
    DEBUG: bool = bool(os.getenv("DEBUG", False))
    
    # CORS Origins
    ALLOWED_ORIGINS: list = [
        "http://localhost",
        "http://localhost:3000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000"
    ]
    
    # Model Paths
    MODEL_PATH: str = os.getenv("MODEL_PATH", "./ml_model/model.pkl")
    
    class Config:
        env_file = ".env"

settings = Settings()