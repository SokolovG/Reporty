import uvicorn
from dishka import make_async_container
from dishka.integrations.litestar import setup_dishka, LitestarProvider
from litestar import Litestar, Request
from litestar.types import ASGIApp
from litestar.middleware import DefineMiddleware
from litestar import Response

from backend.src.api.middleware import ErrorHandlerMiddleware, JWTAuthenticationMiddleware
from backend.src.cli.base import cli
from backend.src.core.exceptions import ApiException
from backend.src.core.plugins import get_sqlalchemy_plugin, admin_plugin
from backend.src.api.responses.base_responses import ErrorResponse
from backend.src.api.routes import (
    record_router,
    report_router,
    task_router,
    profile_router,
    auth_router,
)
from backend.src.core.configs import (
    get_sqlalchemy_config,
    logging_config,
    openapi_config,
    cors_config,
)
from backend.src.core.dependencies import MyProvider

sqlalchemy_plugin = get_sqlalchemy_plugin()
sqlalchemy_config = get_sqlalchemy_config()


def api_exception_handler(request: Request, exc: ApiException) -> Response:
    """Handle ApiException and return proper JSON response."""
    error_response = ErrorResponse(
        error_code=exc.error_code,
        message=exc.message,
        success=False,
        details=exc.details,
    )
    return Response(
        content=error_response, status_code=exc.status_code, media_type="application/json"
    )


def create_app() -> ASGIApp:
    container = make_async_container(MyProvider(), LitestarProvider())

    app = Litestar(
        route_handlers=[
            report_router,
            task_router,
            record_router,
            profile_router,
            auth_router,
        ],
        middleware=[ErrorHandlerMiddleware, DefineMiddleware(JWTAuthenticationMiddleware)],
        plugins=[sqlalchemy_plugin, admin_plugin],
        exception_handlers={ApiException: api_exception_handler},
        debug=True,
        logging_config=logging_config,
        cors_config=cors_config,
        openapi_config=openapi_config,
    )

    setup_dishka(container, app)
    return app


app = create_app()

if __name__ == "__main__":
    cli()
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
