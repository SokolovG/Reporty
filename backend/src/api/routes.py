from litestar import Router

from backend.src.api.controllers import (
    RecordController,
    ReportController,
    TaskController,
)

report_router = Router(path="v1/reports", route_handlers=[ReportController])
task_router = Router(path="v1/tasks", route_handlers=[TaskController])
record_router = Router(path="v1/records", route_handlers=[RecordController])
