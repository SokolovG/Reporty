from dataclasses import dataclass, field
from datetime import datetime

from backend.src.domain.exceptions import (
    RecordAlreadyApprovedError,
    RecordAlreadyProcessedError,
    RecordNotProcessedError,
)


@dataclass
class DailyRecord:
    """Domain entity representing a daily work record.

    Business Rules:
    - Approved records cannot be modified
    - Records must be processed before approval
    - External tasks can only be linked to non-approved records
    """

    id: int
    user_id: int

    title: str
    raw_input: str

    ai_processed: str | None = None
    is_processed: bool = False
    processed_at: datetime | None = None

    is_approved: bool = False
    final_description: str | None = None

    external_task_id: int | None = None
    external_url: str | None = None

    status: str = "OPEN"

    created_at: datetime = field(default_factory=datetime.now)

    def mark_as_processed(self, ai_result: str) -> None:
        """Mark record as processed by AI.

        Business Rule: Cannot process already approved records.

        Args:
            ai_result: The AI-processed version of the record

        Raises:
            RecordAlreadyApprovedError: If record is already approved
            RecordAlreadyProcessedError: If record is already processed
        """
        if self.is_approved:
            raise RecordAlreadyApprovedError(self.id)

        if self.is_processed:
            raise RecordAlreadyProcessedError(self.id)

        self.ai_processed = ai_result
        self.is_processed = True
        self.processed_at = datetime.now()

    def approve(self, final_description: str | None = None) -> None:
        """Approve the record for reporting.

        Business Rule: Can only approve processed records.

        Args:
            final_description: Optional final description, defaults to AI processed version

        Raises:
            RecordNotProcessedError: If record hasn't been processed yet
        """
        if not self.is_processed:
            raise RecordNotProcessedError(self.id)

        self.is_approved = True
        self.final_description = final_description or self.ai_processed

    def can_be_edited(self) -> bool:
        """Check if record can be edited.

        Returns:
            True if record is not approved, False otherwise
        """
        return not self.is_approved

    def link_external_task(self, task_id: int, url: str | None = None) -> None:
        """Link record to an external task.

        Business Rule: Cannot link external tasks to approved records.

        Args:
            task_id: ID of the external task
            url: Optional URL to the external task

        Raises:
            RecordAlreadyApprovedError: If record is already approved
        """
        if not self.can_be_edited():
            raise RecordAlreadyApprovedError(self.id)

        self.external_task_id = task_id
        if url:
            self.external_url = url

    def unlink_external_task(self) -> None:
        """Remove link to external task.

        Business Rule: Cannot unlink external tasks from approved records.

        Raises:
            RecordAlreadyApprovedError: If record is already approved
        """
        if not self.can_be_edited():
            raise RecordAlreadyApprovedError(self.id)

        self.external_task_id = None
        self.external_url = None

    def close(self) -> None:
        """Close the record.

        Closed records are considered complete but can still be edited if not approved.
        """
        self.status = "CLOSED"

    def reopen(self) -> None:
        """Reopen a closed record.

        Business Rule: Cannot reopen approved records.

        Raises:
            RecordAlreadyApprovedError: If record is already approved
        """
        if self.is_approved:
            raise RecordAlreadyApprovedError(self.id)

        self.status = "OPEN"

    def update_content(self, title: str | None = None, raw_input: str | None = None) -> None:
        """Update record content.

        Business Rule: Cannot update approved records.

        Args:
            title: New title for the record
            raw_input: New raw input text

        Raises:
            RecordAlreadyApprovedError: If record is already approved
        """
        if not self.can_be_edited():
            raise RecordAlreadyApprovedError(self.id)

        if title is not None:
            self.title = title

        if raw_input is not None:
            self.raw_input = raw_input
            self.is_processed = False
            self.ai_processed = None
            self.processed_at = None

    def append_content(self, additional_text: str, separator: str = ", ") -> None:
        """Append additional content to raw input.

        Business Rule: Cannot append to approved records.

        Args:
            additional_text: Text to append
            separator: Separator between existing and new content

        Raises:
            RecordAlreadyApprovedError: If record is already approved
        """
        if not self.can_be_edited():
            raise RecordAlreadyApprovedError(self.id)

        self.raw_input = f"{self.raw_input}{separator}{additional_text}"

        self.is_processed = False
        self.ai_processed = None
        self.processed_at = None
