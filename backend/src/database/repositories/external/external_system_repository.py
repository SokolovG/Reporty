from advanced_alchemy import repository

from backend.src.database.models import ExternalSystem


class ExternalSystemRepository(repository.SQLAlchemyAsyncRepository[ExternalSystem]):  # type: ignore
    model_type: type[ExternalSystem] = ExternalSystem
