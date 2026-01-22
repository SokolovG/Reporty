import msgspec


class UserResponse(msgspec.Struct):
    """User data for API responses."""

    name: str
    email: str
    id: int
    is_active: bool
    is_verify: bool
    display_name: str | None = None
    department: str | None = None
    position: str | None = None
    ai_auto_process: bool = False
    ai_provider_id: int | None = None
    ai_model_id: int | None = None
    custom_prompt: str | None = None


class AccessTokenResponse(msgspec.Struct):
    access_token: str
