from typing import Any, Dict


class ApiException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: str = "API_ERROR",
        details: Dict[str, Any] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)


class AuthenticationError(ApiException):
    def __init__(
        self, message: str = "Authentication failed", details: Dict[str, Any] | None = None
    ):
        super().__init__(message, 401, "AUTH_ERROR", details)


class AuthorizationError(ApiException):
    def __init__(self, message: str = "Access denied", details: Dict[str, Any] | None = None):
        super().__init__(message, 403, "FORBIDDEN", details)


class ValidationError(ApiException):
    def __init__(self, message: str = "Validation failed", details: Dict[str, Any] | None = None):
        super().__init__(message, 400, "VALIDATION_ERROR", details)


class NotFoundError(ApiException):
    def __init__(
        self, resource: str, resource_id: Any | None = None, details: Dict[str, Any] | None = None
    ):
        message = f"{resource} not found"
        if resource_id is not None:
            message += f" with id: {resource_id}"

        context = {"resource": resource, "resource_id": resource_id}
        if details:
            context.update(details)

        super().__init__(message, 404, "NOT_FOUND", context)


class ConflictError(ApiException):
    def __init__(self, message: str = "Resource conflict", details: Dict[str, Any] | None = None):
        super().__init__(message, 409, "CONFLICT", details)


class InternalServerError(ApiException):
    def __init__(
        self, message: str = "Internal server error", details: Dict[str, Any] | None = None
    ):
        super().__init__(message, 500, "INTERNAL_ERROR", details)
