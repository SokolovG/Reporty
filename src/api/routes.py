from litestar import Router

from src.api.record_controller import RecordController
from src.api.report_controller import ReportController
from src.api.task_controller import TaskController

report_router = Router(path="auth", route_handlers=[ReportController])
task_router = Router(path="user", route_handlers=[TaskController])
record_router = Router(path="user", route_handlers=[RecordController])
