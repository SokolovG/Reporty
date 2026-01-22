from dataclasses import dataclass, field
from datetime import datetime

from backend.src.domain.exceptions import NoRecordsForReportError, ReportGenerationError


@dataclass
class Report:
    """Domain entity representing a generated report.

    Business Rules:
    - Reports must have at least one record
    - Report content cannot be empty
    """

    id: int
    user_id: int

    report_date: datetime
    content: str

    entries_count: int = 0
    generated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate report after initialization."""
        if self.entries_count == 0:
            raise NoRecordsForReportError(self.report_date.strftime("%Y-%m-%d"))

        if not self.content or self.content.strip() == "":
            raise ReportGenerationError("Report content cannot be empty")

    @classmethod
    def create(
        cls,
        user_id: int,
        report_date: datetime,
        content: str,
        entries_count: int,
        report_id: int = 0,
    ) -> "Report":
        """Factory method to create a new report.

        Args:
            user_id: ID of the user generating the report
            report_date: Date for which the report is generated
            content: Generated report content
            entries_count: Number of records included in the report
            report_id: ID of the report (0 for new reports)

        Returns:
            New Report instance

        Raises:
            NoRecordsForReportError: If entries_count is 0
            ReportGenerationError: If content is empty
        """
        return cls(
            id=report_id,
            user_id=user_id,
            report_date=report_date,
            content=content,
            entries_count=entries_count,
            generated_at=datetime.now(),
        )

    def is_empty(self) -> bool:
        """Check if report has no entries."""
        return self.entries_count == 0

    def get_summary(self) -> str:
        """Get a brief summary of the report."""
        date_str = self.report_date.strftime("%Y-%m-%d")
        return f"Report for {date_str} with {self.entries_count} entries"
