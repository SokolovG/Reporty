from dataclasses import dataclass
from datetime import datetime

from backend.src.domain.exceptions import InvalidExternalTaskError


@dataclass
class ExternalTask:
    """Domain entity representing a task from an external system.

    Business Rules:
    - External ID and system ID are required
    - URL must be valid
    - Sync timestamp must be updated on each sync
    """

    id: int
    user_id: int
    external_id: int
    external_system_id: int

    title: str
    description: str | None = None
    status: str = "TODO"
    url: str = ""

    external_created_at: datetime = datetime.now()
    external_updated_at: datetime | None = None
    completed_at: datetime | None = None

    last_sync: datetime = datetime.now()

    def __post_init__(self) -> None:
        """Validate external task after initialization."""
        if not self.url or self.url.strip() == "":
            raise InvalidExternalTaskError(
                "URL is required", details={"external_id": self.external_id}
            )

        if not self.title or self.title.strip() == "":
            raise InvalidExternalTaskError(
                "Title is required", details={"external_id": self.external_id}
            )

    def mark_as_synced(self) -> None:
        """Mark task as synchronized with external system."""
        self.last_sync = datetime.now()

    def update_from_external(
        self,
        title: str | None = None,
        description: str | None = None,
        status: str | None = None,
        external_updated_at: datetime | None = None,
    ) -> None:
        """Update task information from external system.

        Args:
            title: Updated title
            description: Updated description
            status: Updated status
            external_updated_at: Timestamp of last update in external system
        """
        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if status is not None:
            self.status = status

        if external_updated_at is not None:
            self.external_updated_at = external_updated_at

        self.mark_as_synced()

    def mark_as_completed(self) -> None:
        """Mark task as completed."""
        if self.completed_at is None:
            self.completed_at = datetime.now()
            self.status = "DONE"

    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.completed_at is not None

    def needs_sync(self, max_age_hours: int = 24) -> bool:
        """Check if task needs to be synchronized.

        Args:
            max_age_hours: Maximum age in hours before sync is needed

        Returns:
            True if task needs sync, False otherwise
        """
        age = datetime.now() - self.last_sync
        return age.total_seconds() > (max_age_hours * 3600)
