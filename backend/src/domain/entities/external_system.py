from dataclasses import dataclass


@dataclass
class ExternalSystem:
    """Domain entity representing an external task management system.

    Business Rules:
    - System name must be unique
    - API configuration must be valid
    - Inactive systems cannot be used
    """

    id: int
    name: str
    display_name: str

    api_config: dict
    is_active: bool = True

    def activate(self) -> None:
        """Activate the external system."""
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate the external system."""
        self.is_active = False

    def update_config(self, api_config: dict) -> None:
        """Update API configuration.

        Args:
            api_config: New API configuration dictionary
        """
        self.api_config = api_config

    def is_configured(self) -> bool:
        """Check if system is properly configured.

        Returns:
            True if system has API configuration, False otherwise
        """
        return bool(self.api_config) and self.is_active
