import logging
import msgspec
from litestar.middleware.base import AbstractMiddleware
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.exceptions import HTTPException
from litestar.types import Scope, Receive, Send
from backend.src.core.exceptions import ApiException
from backend.src.api.responses.base_responses import ErrorResponse


class ErrorHandlerMiddleware(AbstractMiddleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            logging.exception(f"Unhandled exception in {scope.get('path', 'unknown')}: {exc}")
            if isinstance(exc, ApiException):
                error_response = ErrorResponse(
                    error_code=exc.error_code,
                    message=exc.message,
                    success=False,
                    details=exc.details,
                )
                status_code = exc.status_code
            elif isinstance(exc, HTTPException):
                error_response = ErrorResponse(
                    success=False,
                    error_code=f"HTTP_{exc.status_code}",
                    message=exc.detail or "HTTP error occurred",
                    details={"status_code": exc.status_code},
                )
                status_code = exc.status_code
            else:
                error_response = ErrorResponse(
                    success=False,
                    error_code="INTERNAL_ERROR",
                    message="An unexpected error occurred",
                    details={"error_type": type(exc).__name__},
                )
                status_code = HTTP_500_INTERNAL_SERVER_ERROR

            response_body = msgspec.json.encode(msgspec.to_builtins(error_response))

            await send(
                {
                    "type": "http.response.start",
                    "status": status_code,
                    "headers": [[b"content-type", b"application/json"]],
                }
            )

            await send(
                {
                    "type": "http.response.body",
                    "body": response_body,
                }
            )
