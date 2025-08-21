from typing import Any
from litestar import Request, Response
from litestar.middleware.base import BaseHTTPMiddleware
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.exceptions import HTTPException, LitestarException
from litestar.responses import JSONResponse

from backend.src.core.exceptions import ApiException
from backend.src.api.responses.base_responses import ErrorResponse


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def __call__(self, scope: dict, receive: Any, send: Any) -> None:
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            request = Request(scope) if scope.get("type") == "http" else None

            if isinstance(exc, ApiException):
                error_response = ErrorResponse(
                    success=False,
                    error_code=exc.error_code,
                    message=exc.message,
                    details=exc.details,
                )

                response = JSONResponse(
                    content=error_response.model_dump(), status_code=exc.status_code
                )

                await response(scope, receive, send)
                return

            elif isinstance(exc, HTTPException):
                error_response = ErrorResponse(
                    success=False,
                    error_code=f"HTTP_{exc.status_code}",
                    message=exc.detail or "HTTP error occurred",
                    details={"status_code": exc.status_code},
                )

                response = JSONResponse(
                    content=error_response.model_dump(), status_code=exc.status_code
                )

                await response(scope, receive, send)
                return

            else:
                error_response = ErrorResponse(
                    success=False,
                    error_code="INTERNAL_ERROR",
                    message="An unexpected error occurred",
                    details={"error_type": type(exc).__name__},
                )

                response = JSONResponse(
                    content=error_response.model_dump(), status_code=HTTP_500_INTERNAL_SERVER_ERROR
                )

                await response(scope, receive, send)
                return
