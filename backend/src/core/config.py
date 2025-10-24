from advanced_alchemy.config import AsyncSessionConfig
from advanced_alchemy.extensions.litestar import EngineConfig
from dotenv import load_dotenv
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.logging import LoggingConfig
from sqlalchemy import Engine, create_engine

from backend.src.core.settings import settings
from backend.src.database.base import Base

load_dotenv()


def get_sqlalchemy_config() -> SQLAlchemyAsyncConfig:
    """Get SQLAlchemy config."""
    return SQLAlchemyAsyncConfig(
        connection_string=settings.async_database_url,
        create_all=False,
        metadata=Base.metadata,
        engine_config=EngineConfig(echo=False),
        before_send_handler="autocommit",
        session_config=AsyncSessionConfig(expire_on_commit=False),
    )


def get_sqlalchemy_plugin() -> SQLAlchemyPlugin:
    """Get SQLAlchemy plugin."""
    return SQLAlchemyPlugin(config=get_sqlalchemy_config())


logging_config = LoggingConfig(
    root={"level": "INFO", "handlers": ["rich_console"]},
    handlers={
        "rich_console": {
            "class": "rich.logging.RichHandler",
            "level": "DEBUG",
            "rich_tracebacks": True,
            "show_path": False,
            "show_time": True,
        },
    },
    log_exceptions="always",
)


def get_sync_engine() -> Engine:
    """Get synchronous engine for SQLAdmin."""
    sync_url = settings.database_url
    return create_engine(sync_url, echo=settings.DEBUG)
