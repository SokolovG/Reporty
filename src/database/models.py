from datetime import UTC, datetime

from litestar_users.adapter.sqlalchemy.mixins import SQLAlchemyUserMixin
from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class DailyRecord(Base):
    """Daily developer record."""

    __tablename__ = "daily_records"

    raw_input: Mapped[str] = mapped_column(
        Text, nullable=False, comment="Original developer record"
    )

    ai_processed: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="AI processed version"
    )

    final_description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="Final description for report"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(UTC), comment="Creation time"
    )
    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="AI processing time"
    )

    is_processed: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Whether processed by AI"
    )
    is_approved: Mapped[bool] = mapped_column(
        Boolean, default=False, comment="Whether approved by user"
    )

    # Связь с внешней задачей (опционально)
    external_task_id: Mapped[int | None] = mapped_column(
        ForeignKey("external_tasks.id"), nullable=True, comment="Link to external task"
    )

    # Relationship
    external_task: Mapped["ExternalTask | None"] = relationship(
        "ExternalTask", back_populates="daily_records"
    )

    def __repr__(self) -> str:
        return (
            f"<DailyRecord(id={self.id}, raw_input='{self.raw_input[:50]}...',"
            f" is_processed={self.is_processed})>"
        )


class ExternalSystem(Base):
    """External task management system (Bitrix, Jira, Asana, etc.)."""

    __tablename__ = "external_systems"

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="System identifier (bitrix, jira, asana)",
    )
    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Human-readable name (Bitrix24, Jira Cloud)",
    )
    api_config: Mapped[dict] = mapped_column(
        JSON, nullable=False, comment="API connection settings"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, comment="Whether system is active"
    )

    # Relationships
    tasks: Mapped[list["ExternalTask"]] = relationship(
        "ExternalTask", back_populates="system", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<ExternalSystem(name='{self.name}', display_name='{self.display_name}',"
            f" active={self.is_active})>"
        )


class ExternalTask(Base):
    """Task from external task management system."""

    __tablename__ = "external_tasks"

    external_id: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Task ID in external system"
    )
    external_system_id: Mapped[int] = mapped_column(
        ForeignKey("external_systems.id"),
        nullable=False,
        comment="Link to external system",
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False, comment="Task title")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Task description")
    status: Mapped[str] = mapped_column(String(100), nullable=False, comment="Task status")

    # Dates
    external_created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="Creation date in external system"
    )
    external_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="Last update in external system"
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="Completion date"
    )

    # Synchronization
    last_sync: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(UTC),
        comment="Last synchronization with external system",
    )

    # Relationships
    system: Mapped["ExternalSystem"] = relationship("ExternalSystem", back_populates="tasks")
    daily_records: Mapped[list["DailyRecord"]] = relationship(
        "DailyRecord", back_populates="external_task"
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("external_system_id", "external_id", name="uk_external_system_task"),
        Index("ix_external_tasks_status", "status"),
        Index("ix_external_tasks_sync", "last_sync"),
    )

    def __repr__(self) -> str:
        return (
            f"<ExternalTask(external_id='{self.external_id}', "
            f"system='{self.system.name if self.system else 'Unknown'}', "
            f"title='{self.title[:30]}...', status='{self.status}')>"
        )


class Report(Base):
    """Generated a daily/weekly report."""

    __tablename__ = "reports"

    report_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="Report date")

    content: Mapped[str] = mapped_column(Text, nullable=False, comment="Generated report content")

    # Metadata
    entries_count: Mapped[int] = mapped_column(
        default=0, comment="Number of included daily records"
    )
    generated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(UTC), comment="Report generation time"
    )

    # Indexes for performance
    __table_args__ = (
        Index("ix_reports_date", "report_date"),
        Index("ix_reports_generated", "generated_at"),
    )

    def __repr__(self) -> str:
        return (
            f"<Report(id={self.id}, report_date={self.report_date.date()}, "
            f"entries_count={self.entries_count})>"
        )


class User(Base, SQLAlchemyUserMixin):
    """Application user."""

    __tablename__ = "users"
