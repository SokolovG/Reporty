import uvicorn
from dishka import make_async_container
from dishka.integrations.litestar import LitestarProvider, setup_dishka
from litestar import Litestar, Request, Response
from litestar.middleware import DefineMiddleware
from litestar.types import ASGIApp

from backend.src.infrastructure.config.configs import (
    cors_config,
    get_sqlalchemy_config,
    logging_config,
    openapi_config,
)
from backend.src.infrastructure.config.plugins import admin_plugin, get_sqlalchemy_plugin
from backend.src.infrastructure.di.dependencies import MyProvider
from backend.src.infrastructure.exceptions.api_exceptions import ApiException
from backend.src.presentation.middleware.authentication import JWTAuthenticationMiddleware
from backend.src.presentation.middleware.error_handler import ErrorHandlerMiddleware
from backend.src.presentation.responses.base_responses import ErrorResponse
from backend.src.presentation.routes import (
    auth_router,
    profile_router,
    record_router,
    report_router,
    task_router,
)

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
        # exception_handlers: ExceptionHandlersMap | None = None, ExceptionHandlersMap: TypeAlias = "MutableMapping[Union[int, Type[Exception]], ExceptionHandler]"
        exception_handlers={ApiException: api_exception_handler},  # ty: ignore
        debug=True,
        logging_config=logging_config,
        cors_config=cors_config,
        openapi_config=openapi_config,
    )

    setup_dishka(container, app)
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
