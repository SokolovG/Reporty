from litestar import Router

from src.api.controllers import RecordController, ReportController, TaskController

report_router = Router(path="report", route_handlers=[ReportController])
task_router = Router(path="task", route_handlers=[TaskController])
record_router = Router(path="record", route_handlers=[RecordController])
