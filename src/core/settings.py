import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings from environment variables."""

    """Application settings from environment variables."""

    # Database
    db_host: str = os.getenv("DB_HOST", "db")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "reporty")
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASSWORD", "password")

    # Application
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    secret_key: str = os.getenv("SECRET_KEY", "")

    # LLM API
    ai_api_key: str | None = os.getenv("AI_API_KEY", None)

    # Bitrix24
    bitrix_webhook_url: str | None = os.getenv("BITRIX_WEBHOOK_URL", None)
    bitrix_user_id: str | None = os.getenv("BITRIX_USER_ID", None)

    # Feature flags
    enable_bitrix_integration: bool = os.getenv("ENABLE_BITRIX", "False").lower() == "true"
    enable_ai_processing: bool = os.getenv("ENABLE_AI", "True").lower() == "true"

    @property
    def database_url(self) -> str:
        """Synchronous URL for migrations and admin panel."""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def async_database_url(self) -> str:
        """An asynchronous URL for the app to run."""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    def validate_claude_settings(self) -> bool:
        """Check your Claude API settings."""
        return self.enable_ai_processing and self.ai_api_key is not None

    def validate_bitrix_settings(self) -> bool:
        """Check Bitrix24 settings."""
        return (
            self.enable_bitrix_integration
            and self.bitrix_webhook_url is not None
            and self.bitrix_user_id is not None
        )


settings = Settings()
