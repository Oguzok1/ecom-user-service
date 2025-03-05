from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Container

from ecom_user_service.config import Settings
from .gateways import GatewaysContainer
from .repositories import RepositoriesContainer
from .services import ServicesContainer


class ApplicationContainer(DeclarativeContainer):
    """
    Application container.
    Register all routes in wiring_config.
    """

    wiring_config = WiringConfiguration(
        modules=[
            "ecom_user_service.routers.v1.auth",
            "ecom_user_service.routers.v1.user",
            "ecom_user_service.security",
        ]
    )

    config: Configuration = Configuration(pydantic_settings=[Settings()])
    gateways: GatewaysContainer = Container(GatewaysContainer, config=config)

    repositories: Container[RepositoriesContainer] = Container(
        RepositoriesContainer, config=config, gateways=gateways
    )
    services: ServicesContainer = Container(
        ServicesContainer, config=config, gateways=gateways, repositories=repositories
    )
