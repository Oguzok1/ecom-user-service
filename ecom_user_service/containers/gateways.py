from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton

from ecom_user_service.config import DBSettings
from ecom_user_service.gateways.db import Database

class GatewaysContainer(DeclarativeContainer):
    """Gateways container."""

    config: Configuration = Configuration()

    db: Singleton[Database] = Singleton[Database](
        Database,
        url=config.db.url
    )
