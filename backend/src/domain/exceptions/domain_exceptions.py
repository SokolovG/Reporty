from typing import Any


class DomainException(Exception):
    """Base exception for domain layer"""

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class RecordAlreadyApprovedError(DomainException):
    """Raised when trying to modify approved record"""

    def __init__(self, message: str):
        super().__init__(message)


class RecordNotProcessedError(DomainException):
    """Raised when trying to approve unprocessed record"""

    def __init__(self, message: str):
        super().__init__(message)


class UserAlreadyActiveError(DomainException):
    """Raised when trying to activate already active user"""

    def __init__(self, message: str):
        super().__init__(message)


class EmailAlreadyVerifiedError(DomainException):
    """Raised when trying to verify already verified email"""

    def __init__(self, message: str):
        super().__init__(message)


class UserCannotUseAIError(DomainException):
    """Raised when user tries to use AI without proper setup"""

    def __init__(self, message: str):
        super().__init__(message)


class UserNotActiveError(DomainException):
    """Raised when inactive user tries to perform actions requiring active status"""

    def __init__(self, message: str):
        super().__init__(message)


class ReportGenerationError(DomainException):
    """Raised when report generation fails"""

    def __init__(self, message: str):
        super().__init__(message)


class NoRecordsForReportError(DomainException):
    """Raised when trying to generate a report with no records"""

    def __init__(self, message: str):
        super().__init__(message)


class InvalidExternalTaskError(DomainException):
    """Raised when external task data is invalid"""

    def __init__(self, message: str):
        super().__init__(message)
