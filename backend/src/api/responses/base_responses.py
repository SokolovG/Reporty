from typing import Any, Literal
import msgspec


class SuccessResponse(msgspec.Struct):
    success: Literal[True] = True
    data: dict[str, Any] | None = None
    message: str | None = None


class ErrorResponse(msgspec.Struct):
    success: Literal[False] = False
    error_code: str
    message: str
    details: dict[str, Any] | None = None
