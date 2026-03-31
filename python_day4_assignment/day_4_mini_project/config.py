from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "LoanHub"
    DEBUG: bool = False
    DATABASE_URL: str
    LOG_LEVEL: str = "INFO"
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin1234"
    ADMIN_EMAIL: str = "admin@loanhub.com"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()