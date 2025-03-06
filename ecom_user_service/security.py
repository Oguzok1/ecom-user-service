from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.security import APIKeyCookie

from ecom_user_service.containers.application import ApplicationContainer
from ecom_user_service.models import User
from ecom_user_service.services.auth import AuthService


class Security:
    cookie_scheme = APIKeyCookie(name="token")

    @inject
    async def __call__(
        self,
        token: str = Depends(cookie_scheme),
        service: AuthService = Depends(
            Provide[ApplicationContainer.services.auth]
        ),
    ) -> User:
        return await service.authenticate(token)
