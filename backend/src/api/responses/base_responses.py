from typing import Any, Literal, Sequence
import msgspec
from msgspec import Struct


class SuccessResponse(msgspec.Struct):
    success: Literal[True] = True
    data: Struct | Sequence[Struct] | dict[str, Any] | None = None
    message: str | None = None


class ErrorResponse(msgspec.Struct):
    error_code: str
    message: str
    success: Literal[False] = False
    details: dict[str, Any] | None = None
