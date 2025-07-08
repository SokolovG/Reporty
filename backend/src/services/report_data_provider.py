from datetime import datetime

from backend.src.database.repositories.profile_settings import ProfileRepository
from backend.src.database.models import DailyRecord, User, Profile
from sqlalchemy import select


class ReportDataProvider:
    def __init__(self, profile_repo: ProfileRepository):
        self.profile_repo = profile_repo

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
        session = self.profile_repo.session
        result = await session.execute(
            select(User, Profile)
            .join(Profile, Profile.user_id == User.id)
            .where(User.id == user_id)
        )
        user, profile = result.first() if result is not None else (None, None)  # type: ignore

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
            "id": user.id,
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
