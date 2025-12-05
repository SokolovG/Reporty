# Domain-based imports
from backend.src.services.auth import AuthService, JWTService, UserService, AdminAuth
from backend.src.services.records import RecordService, TaskService
from backend.src.services.reports import ReportService
from backend.src.services.ai import AIService
from backend.src.services.shared import (
    EncryptionService,
    NotificationService,
    PaginationParams,
    PaginatedResponse,
)
from backend.src.services.settings import SettingsService

__all__ = [
    # Auth domain
    "AuthService",
    "JWTService",
    "UserService",
    "AdminAuth",
    # Records domain
    "RecordService",
    "TaskService",
    # Reports domain
    "ReportService",
    # AI domain
    "AIService",
    # Shared utilities
    "EncryptionService",
    "NotificationService",
    "PaginationParams",
    "PaginatedResponse",
    # Settings domain
    "SettingsService",
]
