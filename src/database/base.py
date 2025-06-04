from advanced_alchemy.base import UUIDAuditBase


class Base(UUIDAuditBase):
    """Base class for models with UUID and audit fields."""

    __abstract__ = True
