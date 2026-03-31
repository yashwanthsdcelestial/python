"""
Settings module using Pydantic BaseSettings.

This module loads configuration from environment variables and .env files.
The Settings class is a singleton that should be used throughout the app.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.
    
    This class acts as a singleton for configuration management.
    All settings are immutable and can be accessed throughout the app.
    
    Attributes:
        app_name: Name of the application
        debug: Debug mode flag
        json_db_path: Path to the JSON database file
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    
    app_name: str = "TaskAPI"
    debug: bool = False
    json_db_path: str = "./data/tasks.json"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        frozen=True  # Make settings immutable
    )


# Singleton instance - used throughout the app
settings = Settings()
