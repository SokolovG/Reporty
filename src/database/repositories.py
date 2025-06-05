from advanced_alchemy import repository

from src.api.dto import DailyRecordRequest
from src.api.dto.report_dto import DailyReportRequest
from src.database.models import DailyRecord, Report


class DailyRecordRepository(repository.SQLAlchemyAsyncRepository[DailyRecord]):  # type: ignore
    model_type: type[DailyRecord] = DailyRecord

    async def create_record(self, dto: DailyRecordRequest) -> DailyRecord:
        record = DailyRecord(
            raw_input=dto.raw_input,
            bitrix_task_id=dto.bitrix_task_id,
        )

        return await self.add(record)


class DailyReportRepository(repository.SQLAlchemyAsyncRepository[Report]):  # type: ignore
    model_type: type[Report] = Report

    async def create_report(self, dto: DailyReportRequest) -> Report:
        record = Report()

        return await self.add(record)
