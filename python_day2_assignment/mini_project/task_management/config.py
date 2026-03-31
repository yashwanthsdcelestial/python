"""Configuration module for FastAPI Task Management System."""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""
    
    app_name: str = "TaskAPI"
    debug: bool = True
    log_level: str = "INFO"
    json_db_path: str = "./data"
    log_file_path: str = "./logs/app.log"
    database_file_users: str = "users.json"
    database_file_tasks: str = "tasks.json"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False
    )
    
    @property
    def users_db_path(self) -> Path:
        """Get full path to users database file."""
        return Path(self.json_db_path) / self.database_file_users
    
    @property
    def tasks_db_path(self) -> Path:
        """Get full path to tasks database file."""
        return Path(self.json_db_path) / self.database_file_tasks
    
    @property
    def log_file(self) -> Path:
        """Get full path to log file."""
        return Path(self.log_file_path)


# Global settings instance
settings = Settings()
