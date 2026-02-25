from advanced_alchemy.config import AsyncSessionConfig
from advanced_alchemy.extensions.litestar import EngineConfig
from dotenv import load_dotenv
from litestar.config.cors import CORSConfig
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig
from litestar.logging import LoggingConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme
from sqlalchemy import Engine, create_engine

from backend.src.infrastructure.config.settings import settings
from backend.src.infrastructure.database.base import Base

load_dotenv()

openapi_config = OpenAPIConfig(
    title="Reporty API",
    version="1.0.0",
    components=Components(
        security_schemes={
            "BearerAuth": SecurityScheme(
                type="http",
                scheme="bearer",
                bearer_format="JWT",
            ),
            "CookieAuth": SecurityScheme(
                type="apiKey",
                name="accessToken",
            ),
        }
    ),
    security=[{"BearerAuth": []}, {"CookieAuth": []}],
)


def get_sqlalchemy_config() -> SQLAlchemyAsyncConfig:
    """Get SQLAlchemy config."""
    return SQLAlchemyAsyncConfig(
        connection_string=settings.async_database_url,
        create_all=False,
        metadata=Base.metadata,
        engine_config=EngineConfig(echo=False),
        # before_send_handler="autocommit",
        session_config=AsyncSessionConfig(expire_on_commit=False),
    )


logging_config = LoggingConfig(
    root={"level": "INFO", "handlers": ["rich_console"]},
    handlers={
        "rich_console": {
            "class": "rich.logging.RichHandler",
            "level": "INFO",
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


cors_config = CORSConfig(
    allow_origins=["http://localhost:5173", "http://0.0.0.0:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["authorization"],
)
