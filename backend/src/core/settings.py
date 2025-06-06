import os
from dataclasses import field

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Database
    db_host: str = os.getenv("DB_HOST", "db")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "reporty")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "password")

    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    secret_key: str = os.getenv("SECRET_KEY", "")

    ai_api_key: str | None = os.getenv("AI_API_KEY", None)

    default_external_system: str | None = os.getenv("DEFAULT_EXTERNAL_SYSTEM", None)

    external_systems_config: dict = field(
        default_factory=lambda: {
            "bitrix": {
                "enabled": os.getenv("BITRIX_ENABLED", "False").lower() == "true",
                "webhook_url": os.getenv("BITRIX_WEBHOOK_URL"),
                "user_id": os.getenv("BITRIX_USER_ID"),
            },
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

    def get_enabled_systems(self) -> list[str]:
        """Get a list of enabled external systems."""
        return [
            system_name
            for system_name, config in self.external_systems_config.items()
            if config.get("enabled", False)
        ]

    @property
    def database_url(self) -> str:
        """Synchronous URL for migrations and admin panel."""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def async_database_url(self) -> str:
        """An asynchronous URL for the app to run."""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    def validate_system_config(self, system_name: str) -> bool:
        """Validate configuration for a specific system."""
        config = self.external_systems_config.get(system_name, {})

        if not config.get("enabled", False):
            return False

        if system_name == "bitrix":
            return all([config.get("webhook_url"), config.get("user_id")])
        elif system_name == "jira":
            return all([config.get("base_url"), config.get("email"), config.get("api_token")])
        elif system_name == "asana":
            return bool(config.get("personal_access_token"))

        return False

    def get_system_config(self, system_name: str) -> dict:
        """Get configuration for a specific system."""
        return self.external_systems_config.get(system_name, {})  # type: ignore


settings = Settings()
