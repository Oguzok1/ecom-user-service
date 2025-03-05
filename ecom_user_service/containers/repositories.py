from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Configuration,
    DependenciesContainer,
    Singleton,
)

from .gateways import GatewaysContainer
from ..repositories.user import UserRepository


class RepositoriesContainer(DeclarativeContainer):
    """Repositories container."""

    config: Configuration = Configuration()
    gateways: GatewaysContainer = DependenciesContainer()

    user: Singleton[UserRepository] = Singleton[UserRepository](
        UserRepository,
        db=gateways.db,
    )
