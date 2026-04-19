from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis .env
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class Settings(BaseSettings):
    """Configuration de l'application via Pydantic Settings."""
    
    # --- CHANGEMENT ICI : On passe de Anthropic à Google Gemini ---
    GOOGLE_API_KEY: str
    APP_API_KEY: str = "Louis882004" 
    MODEL_NAME: str = "gemini-2.0-flash-lite"
    
    # Logique métier et contraintes
    MIN_CONFIDENCE_THRESHOLD: float = 0.85
    MAX_IMAGE_SIZE_MB: int = 5
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    # Données XAF (CFA BEAC)
    XAF_DENOMINATIONS: List[str] = ["500", "1000", "2000", "5000", "10000"]
    
    # Application Info
    APP_NAME: str = "XAF Fake Bill Detector API"
    APP_VERSION: str = "1.1.0"
    CORS_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(extra="ignore")

# Instance globale pour l'application
settings = Settings()