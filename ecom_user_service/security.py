from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ecom_user_service.containers.application import ApplicationContainer
from ecom_user_service.models import User
from ecom_user_service.services.auth import AuthService


class Security:
    bearer = HTTPBearer()

    @inject
    async def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(bearer),
        service: AuthService = Depends(
            Provide[ApplicationContainer.services.auth]
        ),
    ) -> User:
        print(f"{credentials.credentials=}")
        return await service.authenticate(credentials.credentials)
