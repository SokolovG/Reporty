from datetime import datetime

from backend.src.application.use_cases.ai.ai_use_cases import AIUseCases
from backend.src.infrastructure.database.repositories import DailyRecordRepository
from backend.src.infrastructure.exceptions.api_exceptions import InternalServerError
from backend.src.presentation.dto import DailyRecordResponse
from backend.src.presentation.dto.converters import record_to_response


class ProcessRecordWithAIUseCases:
    def __init__(
        self,
        record_repo: DailyRecordRepository,
        ai_use_cases: AIUseCases | None = None,
    ) -> None:
        self.repo = record_repo
        self.ai_use_cases = ai_use_cases

    async def process_with_ai(self, record_id: int, user_id: int) -> DailyRecordResponse:
        """Process record with AI."""
        try:
            record = await self.repo.get_record(record_id=record_id, user_id=user_id)

            if not self.ai_use_cases:
                raise InternalServerError("AI service not available")

            ai_processed = await self.ai_use_cases.process_record(record.raw_input, user_id)
            record.ai_processed = ai_processed
            record.processed_at = datetime.now()
            record.is_processed = True

            updated_record = await self.repo.update(record)
            await self.repo.session.commit()

            return record_to_response(updated_record)
        except Exception as e:
            raise InternalServerError(
                f"Failed to process record with AI: {str(e)}",
                {"record_id": record_id, "user_id": user_id},
            )
