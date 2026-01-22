import msgspec


class UpdateUserData(msgspec.Struct):
    """Request to update user information."""

    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    email: str | None = None


class RegisterData(msgspec.Struct):
    """Request to update user registration data."""

    name: str
    email: str
    password: str


class LoginData(msgspec.Struct):
    """Request for update user login."""

    email: str
    password: str


class ChangePasswordData(msgspec.Struct):
    """Request for update password change."""

    old_password: str
    new_password: str


class TokenInfo(msgspec.Struct):
    """Token information for authentication."""

    access: str
    refresh: str
    token_type: str
