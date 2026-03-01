from dataclasses import dataclass, field
from datetime import datetime

from backend.src.domain.entities.external_task import ExternalTask
from backend.src.domain.exceptions.domain_exceptions import (
    RecordAlreadyApprovedError,
    RecordNotProcessedError,
)
from backend.src.domain.value_objects import RecordStatus


@dataclass
class DailyRecord:
    """Domain entity representing a daily work record"""

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
    external_task: ExternalTask | None = None

    status: RecordStatus = RecordStatus.OPEN

    created_at: datetime = field(default_factory=datetime.now)

    def mark_as_processed(self, ai_result: str) -> None:
        """Mark record as processed by AI

        Business rule: Cannot process already approved record
        """
        if self.is_approved:
            raise RecordAlreadyApprovedError(
                f"Record {self.id} is already approved and cannot be modified"
            )

        self.ai_processed = ai_result
        self.is_processed = True
        self.processed_at = datetime.now()

    def approve(self, final_description: str | None = None) -> None:
        """Approve the record for reporting

        Business rule: Can only approve processed records
        """
        if not self.is_processed:
            raise RecordNotProcessedError(f"Record {self.id} must be processed before approval")

        self.is_approved = True
        self.final_description = final_description or self.ai_processed

    def can_be_edited(self) -> bool:
        """Check if record can be edited"""
        return not self.is_approved

    def link_external_task(self, task_id: int, url: str | None = None) -> None:
        """Link record to external task"""
        if not self.can_be_edited():
            raise RecordAlreadyApprovedError(
                f"Cannot link external task to approved record {self.id}"
            )

        self.external_task_id = task_id
        if url:
            self.external_url = url

    def unlink_external_task(self) -> None:
        """Remove link to external task"""
        if not self.can_be_edited():
            raise RecordAlreadyApprovedError(
                f"Cannot unlink external task from approved record {self.id}"
            )

        self.external_task_id = None
        self.external_url = None

    def close(self) -> None:
        """Close the record"""
        self.status = RecordStatus.CLOSED

    def reopen(self) -> None:
        """Reopen closed record"""
        if self.is_approved:
            raise RecordAlreadyApprovedError(f"Cannot reopen approved record {self.id}")
        self.status = RecordStatus.OPEN
