import uvicorn
from litestar import Litestar
from litestar_users import LitestarUsersPlugin
from sqladmin_litestar_plugin import SQLAdminPlugin

from backend.src.api.routes import record_router, report_router, task_router
from backend.src.core.admin import (
    DailyRecordAdmin,
    ExternalSystemAdmin,
    ExternalTaskAdmin,
    ReportAdmin,
    UserAdmin,
)
from backend.src.core.config import (
    get_sqlalchemy_config,
    get_sqlalchemy_plugin,
    get_sync_engine,
    litestar_users_config,
    logging_config,
)

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
    ],
)
litestar_users = LitestarUsersPlugin(config=litestar_users_config)

app = Litestar(
    route_handlers=[report_router, task_router, record_router],
    plugins=[sqlalchemy_plugin, admin_plugin, litestar_users],
    debug=True,
    logging_config=logging_config,
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
