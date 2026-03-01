from dataclasses import dataclass


@dataclass
class TaskType:
    """Domain entity representing a task type/category.

    Business Rules:
    - Task type title must be unique per user
    - Color must be a valid hex color code if provided
    """

    id: int
    user_id: int

    title: str
    color: str | None = None
    is_active: bool = True

    def activate(self) -> None:
        """Activate the task type."""
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate the task type."""
        self.is_active = False

    def update(self, title: str | None = None, color: str | None = None) -> None:
        """Update task type information.

        Args:
            title: New title for the task type
            color: New color (hex code) for the task type
        """
        if title is not None:
            self.title = title

        if color is not None:
            # Simple validation for hex color
            if color and not color.startswith("#"):
                color = f"#{color}"
            self.color = color
