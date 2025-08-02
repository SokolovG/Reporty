import os
from datetime import timedelta

from advanced_alchemy.config import AsyncSessionConfig
from advanced_alchemy.extensions.litestar import EngineConfig
from dotenv import load_dotenv
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.logging import LoggingConfig
from litestar.security.jwt import JWTCookieAuth
from litestar_users import LitestarUsersConfig
from litestar_users.config import (
    AuthHandlerConfig,
    RegisterHandlerConfig,
    VerificationHandlerConfig,
)
from sqlalchemy import Engine, create_engine

from backend.src.api.dto import UserReadDTO, UserRegistrationDTO, UserUpdateDTO
from backend.src.api.dto.user_dto import AuthenticationSchema
from backend.src.core.settings import settings
from backend.src.database.base import Base
from backend.src.database.models import User
from backend.src.services.user_service import UserService

load_dotenv()


def get_sqlalchemy_config() -> SQLAlchemyAsyncConfig:
    """Get SQLAlchemy config."""
    return SQLAlchemyAsyncConfig(
        connection_string=settings.async_database_url,
        create_all=False,
        metadata=Base.metadata,
        engine_config=EngineConfig(echo=True),
        before_send_handler="autocommit",
        session_config=AsyncSessionConfig(expire_on_commit=False),
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
            "level": "DEBUG",
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
    auth_backend_class=JWTCookieAuth,
    secret=os.getenv("SECRET_KEY", ""),
    user_model=User,  # type: ignore
    user_read_dto=UserReadDTO,
    user_registration_dto=UserRegistrationDTO,
    user_update_dto=UserUpdateDTO,
    user_service_class=UserService,
    authentication_request_schema=AuthenticationSchema,
    auth_handler_config=AuthHandlerConfig(login_path="/api/login", logout_path="/api/logout"),
    register_handler_config=RegisterHandlerConfig(),
    verification_handler_config=VerificationHandlerConfig(),
    user_auth_identifier="username",
    default_token_expiration=timedelta(days=7),
    auth_exclude_paths=[
        "/admin",  # only for development
        "/schema",
        "/schema/",
        "/docs/",
        "/api/login",
    ],  # In the future, delete admin here.
)
