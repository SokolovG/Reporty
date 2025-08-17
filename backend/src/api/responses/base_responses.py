from typing import Any, Literal
import msgspec


class BaseErrorResponse(msgspec.Struct):
    error_code: str


class BaseErrorDetails(msgspec.Struct):
    reason: str
    context: dict[str, Any] = {}


class BaseSuccessResponse(msgspec.Struct):
    status: Literal["success"] = "success"
    data: dict[str, Any] = {}
    message: str | None = None
