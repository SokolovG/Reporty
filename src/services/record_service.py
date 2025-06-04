from uuid import UUID

from src.api.dto import DailyRecordRequest, DailyRecordResponse
from src.database.repositories import DailyRecordRepository


class RecordService:
    def __init__(self, user_repo: DailyRecordRepository) -> None:
        self.repo = user_repo

    async def create_record(self, raw_input: DailyRecordRequest) -> DailyRecordResponse:  # type: ignore
        record = await self.repo.create_record(raw_input)  # noqa

    async def process_with_ai(self, record_id: UUID) -> DailyRecordResponse:  # type: ignore
        pass

    async def approve_record(self, record_id: UUID) -> DailyRecordResponse:  # type: ignore
        pass
