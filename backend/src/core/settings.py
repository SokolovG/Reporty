import os
from dataclasses import field
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    def __init__(self) -> None:
        self.validate_required_secrets()

    # Database
    DB_HOST: str = os.getenv("DB_HOST", "db")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "reporty")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    MASTER_ENCRYPTION_KEY: str = os.getenv("MASTER_ENCRYPTION_KEY", "")
    JWT_PUBLIC_KEY: str = os.getenv("JWT_PUBLIC_KEY", "")
    JWT_PRIVATE_KEY: str = os.getenv("JWT_PRIVATE_KEY", "")
    ALHOTIRHM: str = "RS256"

    DEFAULT_EXTERNAL_SYSTEM: str | None = os.getenv("DEFAULT_EXTERNAL_SYSTEM", None)

    EXTERNAL_SYSTEM_CONFIG: dict = field(
        default_factory=lambda: {
            "jira": {
                "enabled": os.getenv("JIRA_ENABLED", "False").lower() == "true",
                "base_url": os.getenv("JIRA_BASE_URL"),
                "email": os.getenv("JIRA_EMAIL"),
                "api_token": os.getenv("JIRA_API_TOKEN"),
            },
            "asana": {
                "enabled": os.getenv("ASANA_ENABLED", "False").lower() == "true",
                "personal_access_token": os.getenv("ASANA_TOKEN"),
            },
        }
    )

    @property
    def validate_required_secrets(self) -> None:
        required = {
            "SECRET_KEY": self.SECRET_KEY,
            "MASTER_ENCRYPTION_KEY": self.MASTER_ENCRYPTION_KEY,
            "JWT_PUBLIC_KEY": self.JWT_PUBLIC_KEY,
            "JWT_PRIVATE_KEY": self.JWT_PRIVATE_KEY,
        }

        missing = [k for k, v in required.items() if not v]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    def get_enabled_systems(self) -> list[str]:
        """Get a list of enabled external systems."""
        return [
            system_name
            for system_name, config in self.EXTERNAL_SYSTEM_CONFIG.items()
            if config.get("enabled", False)
        ]

    @property
    def database_url(self) -> str:
        """Synchronous URL for migrations and admin panel."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def async_database_url(self) -> str:
        """An asynchronous URL for the app to run."""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def validate_system_config(self, system_name: str) -> bool:
        """Validate configuration for a specific system."""
        config = self.EXTERNAL_SYSTEM_CONFIG.get(system_name, {})

        if not config.get("enabled", False):
            return False

        elif system_name == "jira":
            return all([config.get("base_url"), config.get("email"), config.get("api_token")])
        elif system_name == "asana":
            return bool(config.get("personal_access_token"))

        return False

    def get_system_config(self, system_name: str) -> dict:
        """Get configuration for a specific system."""
        return self.EXTERNAL_SYSTEM_CONFIG.get(system_name, {})  # type: ignore

    class Config:
        mode = os.getenv("MODE", "local")
        env_file = f"backend/.env.{mode}"
        env_file_encoding = "utf-8"


settings = Settings()
