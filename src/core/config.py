from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.logging import LoggingConfig

from src.core.settings import settings
from src.database.base import Base


def get_sqlalchemy_config() -> SQLAlchemyAsyncConfig:
    """Get SQLAlchemy config."""
    return SQLAlchemyAsyncConfig(
        connection_string=settings.database_url, create_all=True, metadata=Base.metadata
    )


def get_sqlalchemy_plugin() -> SQLAlchemyPlugin:
    """Get SQLAlchemy plugin."""
    return SQLAlchemyPlugin(config=get_sqlalchemy_config())


logging_config = LoggingConfig(
    root={"level": "INFO", "handlers": ["console"]},
    formatters={
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
    handlers={
        "console": {
            "class": "logging_config.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
        },
    },
    log_exceptions="always",
)
