import uvicorn
from dishka import make_async_container
from dishka.integrations.litestar import setup_dishka, LitestarProvider
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.types import ASGIApp
from sqladmin_litestar_plugin import SQLAdminPlugin
from litestar.middleware import DefineMiddleware

from backend.src.api.middleware import ErrorHandlerMiddleware, JWTAuthenticationMiddleware
from backend.src.api.routes import (
    record_router,
    report_router,
    task_router,
    settings_router,
    auth_router,
)
from backend.src.core.admin import (
    DailyRecordAdmin,
    ExternalSystemAdmin,
    ExternalTaskAdmin,
    ReportAdmin,
    UserAdmin,
    UserProfileAdmin,
    AIProviderAdmin,
    TaskTypeAdmin,
)
from backend.src.core.config import (
    get_sqlalchemy_config,
    get_sqlalchemy_plugin,
    get_sync_engine,
    logging_config,
)
from backend.src.core.dependencies import MyProvider

sqlalchemy_plugin = get_sqlalchemy_plugin()
sqlalchemy_config = get_sqlalchemy_config()
admin_plugin = SQLAdminPlugin(
    engine=get_sync_engine(),
    base_url="/admin",
    views=[
        DailyRecordAdmin,
        ExternalSystemAdmin,
        ExternalTaskAdmin,
        ReportAdmin,
        UserAdmin,
        UserProfileAdmin,
        AIProviderAdmin,
        TaskTypeAdmin,
    ],
)
cors_config = CORSConfig(
    allow_origins=["http://localhost:5173", "http://0.0.0.0:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["authorization"],
)


def create_app() -> ASGIApp:
    container = make_async_container(MyProvider(), LitestarProvider())

    app = Litestar(
        route_handlers=[
            report_router,
            task_router,
            record_router,
            settings_router,
            auth_router,
        ],
        middleware=[ErrorHandlerMiddleware, DefineMiddleware(JWTAuthenticationMiddleware)],
        plugins=[sqlalchemy_plugin, admin_plugin],
        debug=True,
        logging_config=logging_config,
        cors_config=cors_config,
    )

    setup_dishka(container, app)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
