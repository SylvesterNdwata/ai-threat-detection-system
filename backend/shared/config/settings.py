"""
Configuration settings for the AI Threat Detection System
Uses Pydantic Settings for type-safe configuration management
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings with validation.
    Can be overridden by environment variables or .env file.
    """
    
    # Application
    app_name: str = "AI Threat Detection - Ingestion Service"
    app_version: str = "0.1.0"
    debug: bool = True
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8001
    api_prefix: str = "/api/v1"
    
    # Database
    database_url: str = "sqlite:///./threat_detection.db"
    # For PostgreSQL later: "postgresql://user:password@localhost:5432/threat_detection"
    
    # Kafka (optional for now)
    kafka_bootstrap_servers: Optional[str] = None
    kafka_topic_logs: str = "security-logs"
    kafka_enabled: bool = False
    
    # Security
    max_request_size: int = 10_000_000  # 10MB
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()
