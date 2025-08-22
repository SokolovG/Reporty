import msgspec
from litestar.middleware.base import AbstractMiddleware
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.exceptions import HTTPException
from litestar.responses import JSONResponse
from litestar.types import Scope, Receive, Send

from backend.src.core.exceptions import ApiException
from backend.src.api.responses.base_responses import ErrorResponse


class ErrorHandlerMiddleware(AbstractMiddleware):
    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:  # Правильные типы!
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            if isinstance(exc, ApiException):
                error_response = ErrorResponse(
                    error_code=exc.error_code,
                    message=exc.message,
                    success=False,
                    details=exc.details,
                )

                response_data = msgspec.to_builtins(error_response)

                response = JSONResponse(content=response_data, status_code=exc.status_code)

                await response(scope, receive, send)
                return

            elif isinstance(exc, HTTPException):
                error_response = ErrorResponse(
                    success=False,
                    error_code=f"HTTP_{exc.status_code}",
                    message=exc.detail or "HTTP error occurred",
                    details={"status_code": exc.status_code},
                )

                response_data = msgspec.to_builtins(error_response)

                response = JSONResponse(content=response_data, status_code=exc.status_code)

                await response(scope, receive, send)
                return

            else:
                error_response = ErrorResponse(
                    success=False,
                    error_code="INTERNAL_ERROR",
                    message="An unexpected error occurred",
                    details={"error_type": type(exc).__name__},
                )

                response_data = msgspec.to_builtins(error_response)

                response = JSONResponse(
                    content=response_data, status_code=HTTP_500_INTERNAL_SERVER_ERROR
                )

                await response(scope, receive, send)
                return
