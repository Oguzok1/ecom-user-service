import fastapi
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from ecom_user_service.containers.application import ApplicationContainer
from ecom_user_service.schemas.auth import TokenSchema
from ecom_user_service.schemas.user import UserCreateSchema
from ecom_user_service.services.auth import AuthService

router = fastapi.APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
@inject
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = fastapi.Depends(
        Provide[ApplicationContainer.services.auth]
    ),
) -> TokenSchema:
    return await service.login(
        email=form_data.username,
        raw_password=form_data.password,
    )


@router.post("/register")
@inject
async def register(
    user: UserCreateSchema,
    service: AuthService = fastapi.Depends(
        Provide[ApplicationContainer.services.auth]
    ),
):
    return await service.register(
        email=user.email,
        raw_password=str(user.password),
        age=user.age,
        name=user.name,
        role=user.role,
    )
