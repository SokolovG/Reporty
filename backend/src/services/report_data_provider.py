from datetime import datetime

from sqlalchemy import select

from backend.src.database.repositories.profile_settings import ProfileRepository
from backend.src.database.models import DailyRecord, Profile

from backend.src.database.repositories import UserRepository


class ReportDataProvider:
    def __init__(self, profile_repo: ProfileRepository, user_repo: UserRepository):
        self.profile_repo = profile_repo
        self.user_repo = user_repo

    async def build_context(
        self,
        user_id: int,
        date: datetime,
        records: list[DailyRecord],
        custom_fields: dict | None = None,
    ) -> dict:
        """
        {
            "user": {"id", "email", "full_name", "department"},
            "report_date": datetime,
            "tasks": [{"title", "description", "url", "status"}],
            "metadata": {"total_tasks", "open_tasks", "processed_tasks"},
            "custom": {}  # difficulties, learned, plans и т.д.
        }
        """

        user = self.user_repo.get(user_id)
        profile = self.profile_repo.session.execute(
            select(Profile).where(Profile.user_id == user_id)
        )

        tasks = [
            {
                "title": r.title,
                "description": r.final_description or r.raw_input,
                "url": r.external_url,
                "status": r.status,
            }
            for r in records
        ]

        metadata = {
            "total_tasks": len(records),
            "open_tasks": sum(1 for r in records if r.status == "open"),
            "processed_tasks": sum(1 for r in records if r.is_processed),
        }

        user_data = {
            "email": getattr(user, "email", None),
            "full_name": getattr(user, "name", None),
            "department": getattr(profile, "department", None),
            "position": getattr(profile, "position", None),
        }
        return {
            "user": user_data,
            "report_date": date,
            "tasks": tasks,
            "metadata": metadata,
            "custom": custom_fields or {},
        }
