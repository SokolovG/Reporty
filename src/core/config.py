import os

from dotenv import load_dotenv
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.logging import LoggingConfig
from litestar.security.jwt import JWTAuth
from litestar_users import LitestarUsersConfig
from litestar_users.config import (
    AuthHandlerConfig,
    RegisterHandlerConfig,
    VerificationHandlerConfig,
)
from sqlalchemy import Engine, create_engine

from src.api.dto import UserReadDTO, UserRegistrationDTO, UserUpdateDTO
from src.core.settings import settings
from src.database.base import Base
from src.database.models import User
from src.services.user_service import UserService

load_dotenv()


def get_sqlalchemy_config() -> SQLAlchemyAsyncConfig:
    """Get SQLAlchemy config."""
    return SQLAlchemyAsyncConfig(
        connection_string=settings.async_database_url,
        create_all=True,
        metadata=Base.metadata,
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
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
        },
    },
    log_exceptions="always",
)


def get_sync_engine() -> Engine:
    """Get synchronous engine for SQLAdmin."""
    sync_url = settings.database_url
    return create_engine(sync_url, echo=settings.debug)


litestar_users_config = LitestarUsersConfig(
    auth_backend_class=JWTAuth,
    secret=os.getenv("SECRET_KEY", ""),
    user_model=User,  # type: ignore
    user_read_dto=UserReadDTO,
    user_registration_dto=UserRegistrationDTO,
    user_update_dto=UserUpdateDTO,
    user_service_class=UserService,
    auth_handler_config=AuthHandlerConfig(),
    register_handler_config=RegisterHandlerConfig(),
    verification_handler_config=VerificationHandlerConfig(),
    auth_exclude_paths=["/admin", "/schema"],
)
