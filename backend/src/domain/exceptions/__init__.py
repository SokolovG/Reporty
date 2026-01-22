from backend.src.domain.exceptions.domain_exceptions import (
    DomainException,
    EmailAlreadyVerifiedError,
    ExternalTaskSyncError,
    InvalidExternalTaskError,
    NoRecordsForReportError,
    RecordAlreadyApprovedError,
    RecordAlreadyProcessedError,
    RecordNotProcessedError,
    ReportGenerationError,
    UserAlreadyActiveError,
    UserCannotUseAIError,
    UserNotActiveError,
)

__all__ = [
    "DomainException",
    "RecordAlreadyApprovedError",
    "RecordNotProcessedError",
    "RecordAlreadyProcessedError",
    "UserAlreadyActiveError",
    "UserNotActiveError",
    "EmailAlreadyVerifiedError",
    "UserCannotUseAIError",
    "ReportGenerationError",
    "NoRecordsForReportError",
    "ExternalTaskSyncError",
    "InvalidExternalTaskError",
]
