from advanced_alchemy import repository

from backend.src.infrastructure.database.models import ExternalSystem


class ExternalSystemRepository(repository.SQLAlchemyAsyncRepository[ExternalSystem]):  # ty: ignore
    model_type: type[ExternalSystem] = ExternalSystem
