class DomainException(Exception):
    """Base exception for all domain layer errors."""

    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


class RecordAlreadyApprovedError(DomainException):
    """Raised when trying to modify an already approved record.

    Business rule: Approved records are immutable and cannot be changed.
    """

    def __init__(self, record_id: int):
        super().__init__(
            f"Record {record_id} is already approved and cannot be modified",
            details={"record_id": record_id},
        )


class RecordNotProcessedError(DomainException):
    """Raised when trying to approve a record that hasn't been processed.

    Business rule: Records must be processed by AI before approval.
    """

    def __init__(self, record_id: int):
        super().__init__(
            f"Record {record_id} must be processed before approval",
            details={"record_id": record_id},
        )


class RecordAlreadyProcessedError(DomainException):
    """Raised when trying to process an already processed record.

    Business rule: Records should not be processed multiple times.
    """

    def __init__(self, record_id: int):
        super().__init__(
            f"Record {record_id} has already been processed",
            details={"record_id": record_id},
        )


class UserAlreadyActiveError(DomainException):
    """Raised when trying to activate an already active user.

    Business rule: Active users cannot be activated again.
    """

    def __init__(self, user_id: int):
        super().__init__(
            f"User {user_id} is already active",
            details={"user_id": user_id},
        )


class UserNotActiveError(DomainException):
    """Raised when inactive user tries to perform actions requiring active status."""

    def __init__(self, user_id: int):
        super().__init__(
            f"User {user_id} is not active",
            details={"user_id": user_id},
        )


class EmailAlreadyVerifiedError(DomainException):
    """Raised when trying to verify an already verified email.

    Business rule: Verified emails cannot be verified again.
    """

    def __init__(self, user_id: int, email: str):
        super().__init__(
            f"Email {email} for user {user_id} is already verified",
            details={"user_id": user_id, "email": email},
        )


class UserCannotUseAIError(DomainException):
    """Raised when user tries to use AI without proper configuration.

    Business rule: Users must have AI provider configured to use AI features.
    """

    def __init__(self, user_id: int, reason: str):
        super().__init__(
            f"User {user_id} cannot use AI: {reason}",
            details={"user_id": user_id, "reason": reason},
        )


class ReportGenerationError(DomainException):
    """Raised when report generation fails due to business rules."""

    def __init__(self, reason: str, details: dict | None = None):
        super().__init__(
            f"Cannot generate report: {reason}",
            details=details or {},
        )


class NoRecordsForReportError(DomainException):
    """Raised when trying to generate a report with no records."""

    def __init__(self, date: str):
        super().__init__(
            f"No records found for report on {date}",
            details={"date": date},
        )


class ExternalTaskSyncError(DomainException):
    """Raised when external task synchronization fails."""

    def __init__(self, task_id: int, reason: str):
        super().__init__(
            f"Failed to sync external task {task_id}: {reason}",
            details={"task_id": task_id, "reason": reason},
        )


class InvalidExternalTaskError(DomainException):
    """Raised when external task data is invalid."""

    def __init__(self, reason: str, details: dict | None = None):
        super().__init__(
            f"Invalid external task: {reason}",
            details=details or {},
        )
