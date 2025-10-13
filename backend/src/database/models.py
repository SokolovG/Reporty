from datetime import datetime

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

from backend.src.database.base import Base, RecordStatus


# TODO: USER_ID NULLABLE=FALSE!


class DailyRecord(Base):
    """Daily developer record."""

    __tablename__ = "daily_records"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, comment="ID пользователя"
    )
    title: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="Название задачи/активности"
    )

    raw_input: Mapped[str] = mapped_column(
        Text, nullable=False, comment="Original developer record"
    )

    ai_processed: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="AI processed version"
    )

    final_description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="Final description for report"
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
    status: Mapped[str] = mapped_column(default=RecordStatus.OPEN.value)
    external_url: Mapped[str | None] = mapped_column(
        String(500), nullable=True, comment="Quick external task link"
    )

    external_task_id: Mapped[int | None] = mapped_column(
        ForeignKey("external_tasks.id"), nullable=True, comment="Link to external task"
    )

    # Relationship
    external_task: Mapped["ExternalTask | None"] = relationship(
        "ExternalTask", back_populates="daily_records", lazy="joined"
    )

    def __repr__(self) -> str:
        return (
            f"<DailyRecord(id={self.id}, raw_input='{self.raw_input[:50]}...',"
            f" is_processed={self.is_processed})>"
        )

    def __str__(self) -> str:
        return str(self.title)


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

    def __str__(self) -> str:
        return str(self.name)


class ExternalTask(Base):
    """Task from external task management system."""

    __tablename__ = "external_tasks"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True, comment="ID пользователя"
    )
    external_id: Mapped[int | None] = mapped_column(
        Integer, nullable=True, comment="Task ID in external system"
    )
    external_system_id: Mapped[int] = mapped_column(
        ForeignKey("external_systems.id"),
        nullable=False,
        comment="Link to external system",
    )

    title: Mapped[str | None] = mapped_column(String(500), nullable=True, comment="Task title")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Task description")
    status: Mapped[str] = mapped_column(String(100), nullable=False, comment="Task status")
    url: Mapped[str] = mapped_column(String(256), nullable=False, comment="Task link")
    # Dates
    external_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Creation date in external system",
    )
    external_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="Last update in external system"
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, comment="Completion date"
    )

    # Synchronization
    last_sync: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(),
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
            f"title='{self.title or ''}...', status='{self.status}')>"
        )

    def __str__(self) -> str:
        return self.title if self.title else f"External task {self.external_id}"


class Report(Base):
    """Generated a daily/weekly report."""

    __tablename__ = "reports"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True, comment="User ID")
    report_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="Report date")

    content: Mapped[str] = mapped_column(Text, nullable=False, comment="Generated report content")

    # Metadata
    entries_count: Mapped[int] = mapped_column(
        default=0, comment="Number of included daily records"
    )
    generated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now().replace(microsecond=0), comment="Report generation time"
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

    def __str__(self) -> str:
        return str(self.content[:10])


class AIProvider(Base):
    __tablename__ = "ai_providers"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    base_prompt: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="Basic system prompt."
    )

    model_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    requires_api_key: Mapped[bool] = mapped_column(default=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    encrypted_api_key: Mapped[str] = mapped_column(String(500), nullable=True)

    __table_args__ = (Index("ix_ai_providers_active", "is_active"),)

    def __str__(self) -> str:
        return f"{self.name} {self.model_name}"


class User(Base):
    """Application user."""

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, comment="Username for authentication"
    )
    email: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=True, comment="Email for authentication"
    )
    password_hash: Mapped[str] = mapped_column(String, nullable=False, comment="Password hash")
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verify: Mapped[bool] = mapped_column(Boolean, default=False)

    display_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    position: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ai_auto_process: Mapped[bool] = mapped_column(default=False)
    ai_provider_id: Mapped[int] = mapped_column(ForeignKey("ai_providers.id"), nullable=True)

    # Relationships
    ai_provider: Mapped["AIProvider"] = relationship("AIProvider")
    task_types: Mapped[list["TaskType"]] = relationship(
        "TaskType", back_populates="user", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return str(self.name)


class TaskType(Base):
    __tablename__ = "task_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship("User", back_populates="task_types")

    # Indexes for performance
    __table_args__ = (
        UniqueConstraint("user_id", "title", name="uk_user_task_type"),
        Index("ix_task_types_user_active", "user_id", "is_active"),
    )

    def __str__(self) -> str:
        return str(self.title)
