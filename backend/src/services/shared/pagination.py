from typing import Generic, TypeVar
from dataclasses import dataclass

T = TypeVar("T")


@dataclass
class PaginationParams:
    """Pagination parameters."""

    page: int = 1
    size: int = 20

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size


@dataclass
class PaginatedResponse(Generic[T]):
    """Paginated response wrapper."""

    items: list[T]
    total: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(cls, items: list[T], total: int, params: PaginationParams) -> "PaginatedResponse[T]":
        """Create paginated response from items and params."""
        pages = (total + params.size - 1) // params.size
        return cls(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            pages=pages,
        )
