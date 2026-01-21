import os
from pathlib import Path
from typing import Self

from dotenv import load_dotenv
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    # Database
    DB_HOST: str = os.getenv("DB_HOST", "db")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "reporty")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    SECRET_KEY: str = Field(..., description="Secret key for application")
    MASTER_ENCRYPTION_KEY: str = Field(..., description="Master key for encryption")
    JWT_PUBLIC_KEY: str = Field(..., description="JWT public key")
    JWT_PRIVATE_KEY: str = Field(..., description="JWT private key")
    ALGORITHM: str = "RS256"

    DEFAULT_EXTERNAL_SYSTEM: str | None = os.getenv("DEFAULT_EXTERNAL_SYSTEM", None)

    EXTERNAL_SYSTEM_CONFIG: dict = Field(
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

    @model_validator(mode="after")
    def validate_required_secrets(self) -> Self:
        """Verification of mandatory secrets AFTER initialisation."""
        required = {
            "SECRET_KEY": self.SECRET_KEY,
            "MASTER_ENCRYPTION_KEY": self.MASTER_ENCRYPTION_KEY,
            "JWT_PUBLIC_KEY": self.JWT_PUBLIC_KEY,
            "JWT_PRIVATE_KEY": self.JWT_PRIVATE_KEY,
        }

        missing = [k for k, v in required.items() if not v]
        if missing:
            raise ValueError(f"Missing required secrets: {', '.join(missing)}")

        return self

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
        return self.EXTERNAL_SYSTEM_CONFIG.get(system_name, {})

    model_config = {
        "env_file": f"backend/.env.{os.getenv('MODE', 'local')}",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
        "extra": "ignore",
    }


settings = Settings()
