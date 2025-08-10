"""Утилиты для создания ErrorResponse."""

from typing import Any
from backend.src.api.responses import ErrorResponse
from backend.src.api.responses.base_responses import BaseErrorDetails
from backend.src.core.errors import ErrorCode


def create_error(
    error_code: ErrorCode | str,
    message: str,
    reason: str | None = None,
    context: dict[str, Any] | None = None,
) -> ErrorResponse:
    code = error_code.value if isinstance(error_code, ErrorCode) else error_code

    return ErrorResponse(
        error_code=code,
        msg=message,
        details=BaseErrorDetails(reason=reason or message, context=context or {}),
    )


def auth_error(
    message: str = "Authentication failed", context: dict[str, Any] | None = None
) -> ErrorResponse:
    """Создать ошибку аутентификации."""
    return create_error(ErrorCode.INVALID_CREDENTIALS, message, "Authentication failed", context)


def user_not_found_error(email: str | None = None) -> ErrorResponse:
    """Ошибка - пользователь не найден."""
    context = {"email": email} if email else {}
    return create_error(
        ErrorCode.USER_NOT_EXIST,
        "User not found",
        "User with provided email does not exist",
        context,
    )


def user_already_exists_error(email: str) -> ErrorResponse:
    """Ошибка - пользователь уже существует."""
    return create_error(
        ErrorCode.USER_ALREADY_EXISTS,
        "User already exists",
        "User with provided email already exists",
        {"email": email},
    )


def validation_error(message: str, context: dict[str, Any] | None = None) -> ErrorResponse:
    """Ошибка валидации."""
    return create_error("VALIDATION_ERROR", message, "Validation failed", context)


def not_found_error(resource: str, resource_id: Any | None = None) -> ErrorResponse:
    """Ошибка - ресурс не найден."""
    context = {"resource_id": resource_id} if resource_id else {}
    return create_error(
        "NOT_FOUND",
        f"{resource} not found",
        f"Requested {resource.lower()} does not exist",
        context,
    )


def internal_error(
    message: str = "Internal server error", context: dict[str, Any] | None = None
) -> ErrorResponse:
    """Внутренняя ошибка сервера."""
    return create_error("INTERNAL_ERROR", message, "An internal error occurred", context)
