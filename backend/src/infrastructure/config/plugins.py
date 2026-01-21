from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin
from sqladmin_litestar_plugin import SQLAdminPlugin

from backend.src.core.settings import settings
from backend.src.core.configs import get_sqlalchemy_config, get_sync_engine

from backend.src.core.admin import (
    AIModelAdmin,
    DailyRecordAdmin,
    ExternalSystemAdmin,
    ExternalTaskAdmin,
    ReportAdmin,
    UserAdmin,
    AIProviderAdmin,
    TaskTypeAdmin,
)
from backend.src.services.auth.admin_service import AdminAuth


def get_sqlalchemy_plugin() -> SQLAlchemyPlugin:
    """Get SQLAlchemy plugin."""
    return SQLAlchemyPlugin(config=get_sqlalchemy_config())


admin_plugin = SQLAdminPlugin(
    engine=get_sync_engine(),
    authentication_backend=AdminAuth(secret_key=settings.SECRET_KEY),
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
