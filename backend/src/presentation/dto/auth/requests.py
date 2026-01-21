import msgspec


class ChangePasswordRequest(msgspec.Struct):
    old_password: str
    new_password: str


class LoginRequest(msgspec.Struct):
    email: str
    password: str


class RegisterRequest(msgspec.Struct):
    name: str
    password: str
    email: str


class UserUpdateRequest(msgspec.Struct):
    """Request to update user information."""

    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    email: str | None = None
