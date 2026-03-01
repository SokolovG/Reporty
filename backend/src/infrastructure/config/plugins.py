from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin
from sqladmin_litestar_plugin import SQLAdminPlugin

from backend.src.infrastructure.config.admin import (
    AIModelAdmin,
    AIProviderAdmin,
    DailyRecordAdmin,
    ExternalSystemAdmin,
    ExternalTaskAdmin,
    ReportAdmin,
    TaskTypeAdmin,
    UserAdmin,
)
from backend.src.infrastructure.config.configs import get_sqlalchemy_config, get_sync_engine
from backend.src.infrastructure.config.settings import settings
from backend.src.presentation.middleware.admin import AdminMiddleware


def get_sqlalchemy_plugin() -> SQLAlchemyPlugin:
    """Get SQLAlchemy plugin."""
    return SQLAlchemyPlugin(config=get_sqlalchemy_config())


admin_plugin = SQLAdminPlugin(
    engine=get_sync_engine(),
    authentication_backend=AdminMiddleware(secret_key=settings.SECRET_KEY),
    base_url="/admin",
    views=[
        DailyRecordAdmin,
        ExternalSystemAdmin,
        ExternalTaskAdmin,
        ReportAdmin,
        UserAdmin,
        AIProviderAdmin,
        TaskTypeAdmin,
        AIModelAdmin,
    ],
)
