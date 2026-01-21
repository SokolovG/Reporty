from abc import ABC, abstractmethod


class NotificationService(ABC):
    """Abstract notification service interface."""

    @abstractmethod
    async def send_register_notification(self) -> None:
        """Send registration notification."""
        pass

    @abstractmethod
    async def send_password_reset_notification(self, email: str) -> None:
        """Send password reset notification."""
        pass


class DefaultNotificationService(NotificationService):
    """Default implementation of notification service."""

    async def send_register_notification(self) -> None:
        """Send registration notification."""
        # TODO: Implement actual notification logic
        pass

    async def send_password_reset_notification(self, email: str) -> None:
        """Send password reset notification."""
        # TODO: Implement actual notification logic
        pass
