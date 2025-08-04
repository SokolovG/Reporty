from litestar import Router

from backend.src.api.controllers import (
    RecordController,
    ReportController,
    TaskController,
    SettingsController,
    UserController,
    AuthController,
)

report_router = Router(path="api/v1/reports", route_handlers=[ReportController])
task_router = Router(path="api/v1/tasks", route_handlers=[TaskController])
record_router = Router(path="api/v1/records", route_handlers=[RecordController])
settings_router = Router(path="api/v1/settings", route_handlers=[SettingsController])
user_router = Router(path="api/v1/users", route_handlers=[UserController])
auth_router = Router(path="api/v1/auth", route_handlers=[AuthController])
