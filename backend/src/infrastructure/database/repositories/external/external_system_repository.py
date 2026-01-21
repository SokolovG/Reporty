from advanced_alchemy import repository

from backend.src.infrastructure.database.models import ExternalSystemModel


class ExternalSystemRepository(
    repository.SQLAlchemyAsyncRepository[ExternalSystemModel]  # ty:ignore[invalid-type-arguments]
):
    model_type: type[ExternalSystemModel] = ExternalSystemModel
