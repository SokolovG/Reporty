import msgspec


class UpdateUserData(msgspec.Struct):
    """Request to update user information."""

    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    email: str | None = None


class RegisterData(msgspec.Struct):
    """Request to update user registration data."""

    email: str
    name: str
    password: str
    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    ai_auto_process: bool = False


class LoginData(msgspec.Struct):
    """Request for update user login."""

    email: str
    password: str


class ChangePasswordData(msgspec.Struct):
    """Request for update password change."""

    old_password: str
    new_password: str


class UserData(msgspec.Struct):
    """User data transfer object."""

    email: str
    name: str
    password_hash: str
    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    ai_auto_process: bool = False
    is_admin: bool = False
