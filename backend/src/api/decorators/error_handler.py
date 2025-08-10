from functools import wraps
from typing import Callable, Any
from litestar.response import Response
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from backend.src.api.responses import ErrorResponse


def handle_error_response(
    success_status: int = HTTP_200_OK, error_status_map: dict[str, int] | None = None
) -> Callable:
    """
     Decorator for automatic processing of ErrorResponse.

    Args:
        success_status: HTTP status for successful responses
        error_status_map: Mapping of error codes to HTTP statuses
    """
    if error_status_map is None:
        error_status_map = {
            "INVALID_CREDENTIALS": HTTP_401_UNAUTHORIZED,
            "USER_NOT_EXIST": HTTP_401_UNAUTHORIZED,
            "USER_ALREADY_EXISTS": HTTP_400_BAD_REQUEST,
            "VALIDATION_ERROR": HTTP_400_BAD_REQUEST,
            "NOT_FOUND": HTTP_404_NOT_FOUND,
        }

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Response:
            result = await func(*args, **kwargs)

            if isinstance(result, ErrorResponse):
                status_code = error_status_map.get(
                    result.error_code, HTTP_500_INTERNAL_SERVER_ERROR
                )
                return Response(content=result, status_code=status_code)

            return Response(content=result, status_code=success_status)

        return wrapper

    return decorator


auth_error_handler = handle_error_response(
    error_status_map={
        "INVALID_CREDENTIALS": HTTP_401_UNAUTHORIZED,
        "USER_NOT_EXIST": HTTP_401_UNAUTHORIZED,
        "USER_ALREADY_EXISTS": HTTP_400_BAD_REQUEST,
    }
)

crud_error_handler = handle_error_response(
    error_status_map={
        "NOT_FOUND": HTTP_404_NOT_FOUND,
        "VALIDATION_ERROR": HTTP_400_BAD_REQUEST,
        "INTERNAL_ERROR": HTTP_500_INTERNAL_SERVER_ERROR,
    }
)
