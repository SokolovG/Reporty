from abc import ABC, abstractmethod


class NotificationPort(ABC):
    @abstractmethod
    async def send_register_notification(self) -> None:
        """Send registration notification."""

    @abstractmethod
    async def send_reset_password_notification(self) -> None:
        """Send password reset notification."""

    @abstractmethod
    async def send_ai_processing_complete(self, user_id: int, record_id: int) -> None:
        """Notify user when AI processing is complete."""

    @abstractmethod
    async def send_report_generated(self, user_id: int, report_id: int) -> None:
        """Notify user when report is generated."""
