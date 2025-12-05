class NotificationService:
    async def send_register_notification(self) -> None:
        """Send registration notification."""
        # TODO: Implement email/SMS notification

    async def send_reset_password_notification(self) -> None:
        """Send password reset notification."""
        # TODO: Implement password reset notification

    async def send_ai_processing_complete(self, user_id: int, record_id: int) -> None:
        """Notify user when AI processing is complete."""
        # TODO: Implement AI processing notification

    async def send_report_generated(self, user_id: int, report_id: int) -> None:
        """Notify user when report is generated."""
        # TODO: Implement report generation notification
