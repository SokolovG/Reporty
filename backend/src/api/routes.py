from litestar import Router

from backend.src.api.controllers import (
    RecordController,
    ReportController,
    TaskController,
)

report_router = Router(path="v1/report", route_handlers=[ReportController])
task_router = Router(path="v1/task", route_handlers=[TaskController])
record_router = Router(path="v1/record", route_handlers=[RecordController])
