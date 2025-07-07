from litestar import Router

from backend.src.api.controllers import (
    RecordController,
    ReportController,
    TaskController,
)
from backend.src.api.controllers.report_template_controller import ReportTemplateController

report_router = Router(path="v1/report", route_handlers=[ReportController])
task_router = Router(path="v1/task", route_handlers=[TaskController])
record_router = Router(path="v1/record", route_handlers=[RecordController])
template_router = Router(path="v1/report-template", route_handlers=[ReportTemplateController])
