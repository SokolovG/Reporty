from pydantic.dataclasses import dataclass


@dataclass
class RegisterData:
    """Data for user registration."""

    name: str
    email: str
    password: str


@dataclass
class LoginData:
    """Data for user login."""

    email: str
    password: str


@dataclass
class ChangePasswordData:
    """Data for password change."""

    old_password: str
    new_password: str
