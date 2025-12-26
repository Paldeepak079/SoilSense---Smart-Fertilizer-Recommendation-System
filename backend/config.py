"""
Configuration management with environment validation
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Environment
    environment: str = "development"  # development, staging, production
    
    # Database
    database_url: str
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:3001"
    
    # JWT (for future authentication)
    jwt_secret: str = "change-me-in-production-use-strong-random-string"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    
    # Logging
    log_level: str = "INFO"
    log_to_file: bool = False
    log_file_path: str = "app.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.environment.lower() == "production"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse allowed origins from comma-separated string"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Create global settings instance
# This will validate on import and raise error if required vars missing
try:
    settings = Settings()
except Exception as e:
    print(f"❌ Configuration Error: {e}")
    print("Please check your .env file and ensure all required variables are set.")
    raise
