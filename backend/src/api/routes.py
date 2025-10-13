from litestar import Router

from backend.src.api.controllers import (
    RecordController,
    ReportController,
    TaskController,
    ProfileController,
    AuthController,
)

report_router = Router(path="api/v1/reports", route_handlers=[ReportController])
task_router = Router(path="api/v1/tasks", route_handlers=[TaskController])
record_router = Router(path="api/v1/records", route_handlers=[RecordController])
profile_router = Router(path="api/v1/profile", route_handlers=[ProfileController])
auth_router = Router(path="api/v1/auth", route_handlers=[AuthController])
