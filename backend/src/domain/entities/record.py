from datetime import datetime

from pydantic.dataclasses import dataclass


@dataclass
class DailyRecord:
    id: int
    user_id: int
    title: str
    raw_input: str
    ai_processed: str | None = None
    is_processed: bool = False
    is_approved: bool = False
    processed_at: datetime | None = None
    external_task: ...

    def process_with_ai(self, ai_result: str) -> None:
        if self.is_approved:
            raise ValueError("Cannot process already approved record")

        self.ai_processed = ai_result
        self.is_processed = True
        self.processed_at = datetime.now()

    def approve(self) -> None:
        if not self.is_processed:
            raise ValueError("Cannot approve unprocessed record")

        self.is_approved = True

    def can_be_edited(self) -> bool:
        return not self.is_approved
