from pydantic import BaseModel
from typing import Optional
import os

class APISettings(BaseModel):
    """API configuration settings."""
    # API settings
    API_TITLE: str = "IndieTalk Translation API"
    API_DESCRIPTION: str = "A REST API for Hindi to English translation using IndicTrans model"
    API_VERSION: str = "1.0.0"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True  # Enable debug mode for development
    
    # Model settings
    MODEL_DEVICE: str = "cpu"  # Using CPU version of PyTorch
    DEFAULT_CONFIG: str = "default"  # or "fast" or "high_quality"
    
    # Rate limiting
    RATE_LIMIT: int = 100  # requests per minute

    def __init__(self, **data):
        super().__init__(**data)
        # Load environment variables if .env file exists
        if os.path.exists(".env"):
            from dotenv import load_dotenv
            load_dotenv()
            
        # Override settings from environment variables
        for field in self.model_fields:
            env_val = os.getenv(field.upper())
            if env_val is not None:
                setattr(self, field, env_val)

# Create settings instance
settings = APISettings() 