from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Integer,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for models with int and audit fields."""

    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class AIProviders(Enum):
    CLAUDE = "claude"
    OPEN_AI = "open_ai"
    GEMINI = "gemini"
    GROK = "grok"
    LOCAL = "local"
