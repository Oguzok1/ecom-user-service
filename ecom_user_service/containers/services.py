from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Configuration,
    DependenciesContainer,
    Singleton,
)

from .gateways import GatewaysContainer
from .repositories import RepositoriesContainer
from ..services.auth import AuthService
from ..services.user import UserService


class ServicesContainer(DeclarativeContainer):
    """Services container."""

    config: Configuration = Configuration()
    gateways: GatewaysContainer = DependenciesContainer()
    repositories: RepositoriesContainer = DependenciesContainer()

    auth: Singleton[AuthService] = Singleton[AuthService](
        AuthService,
        db=gateways.db,
        user_repository=repositories.user,
        access_token_ttl_days=config.auth.access_token_ttl_days,
        secret_key=config.auth.secret_key,
    )
    user: Singleton[UserService] = Singleton[UserService](
        UserService,
        db=gateways.db,
        user_repository=repositories.user,
    )
