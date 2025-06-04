from datetime import datetime, UTC

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class DailyRecord(Base):
    """Daily developer record."""

    __tablename__ = "daily_records"

    raw_input: Mapped[str] = mapped_column(Text, nullable=False, comment="Original developer record")

    ai_processed: Mapped[str | None] = mapped_column(Text, nullable=True, comment="AI processed version")

    final_description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Final description for report")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC), comment="Creation time")
    processed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="AI processing time")

    is_processed: Mapped[bool] = mapped_column(Boolean, default=False, comment="Whether processed by AI")
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False, comment="Whether approved by user")

    bitrix_task_id: Mapped[str | None] = mapped_column(String(50), nullable=True, comment="Bitrix task ID")

    def __repr__(self) -> str:
        return f"<DailyRecord(id={self.id}, raw_input='{self.raw_input[:50]}...', is_processed={self.is_processed})>"


class BitrixTask(Base):
    """Task from Bitrix24."""

    __tablename__ = "bitrix_tasks"

    bitrix_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="Bitrix task ID")

    title: Mapped[str] = mapped_column(String(500), nullable=False, comment="Task title")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Task description")
    status: Mapped[str] = mapped_column(String(50), nullable=False, comment="Task status")

    # Date
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="Creation date in Bitrix")
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment="Completion date")

    # Synchronization
    last_sync: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC), comment="Last synchronization")

    # Related Posts
    daily_entries = relationship("DailyRecord", backref="bitrix_task",
                                 foreign_keys="DailyRecord.bitrix_task_id",
                                 primaryjoin="BitrixTask.bitrix_id == DailyRecord.bitrix_task_id")

    def __repr__(self) -> str:
        return f"<BitrixTask(bitrix_id={self.bitrix_id}, title='{self.title}', status='{self.status}')>"


class Report(Base):
    """Generated report."""

    __tablename__ = "reports"

    report_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="Report date")

    content: Mapped[str] = mapped_column(Text, nullable=False, comment="Report content")

    # Metadata
    entries_count: Mapped[int] = mapped_column(default=0, comment="Number of included entries")
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC), comment="Generation time")

    def __repr__(self) -> str:
        return f"<Report(id={self.id}, report_date={self.report_date}, entries_count={self.entries_count})>"