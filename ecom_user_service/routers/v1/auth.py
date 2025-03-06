import fastapi
from dependency_injector.wiring import inject, Provide

from ecom_user_service.containers.application import ApplicationContainer
from ecom_user_service.schemas.auth import TokenSchema, LoginSchema
from ecom_user_service.schemas.user import UserCreateSchema
from ecom_user_service.services.auth import AuthService

router = fastapi.APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
@inject
async def login(
    response: fastapi.Response,
    login_data: LoginSchema,
    service: AuthService = fastapi.Depends(
        Provide[ApplicationContainer.services.auth]
    ),
) -> TokenSchema:
    return await service.login(
        response=response,
        email=login_data.email,
        raw_password=str(login_data.raw_password),
    )


@router.post("/register")
@inject
async def register(
    user: UserCreateSchema,
    service: AuthService = fastapi.Depends(
        Provide[ApplicationContainer.services.auth]
    ),
) -> None:
    return await service.register(
        email=user.email,
        raw_password=str(user.password),
        age=user.age,
        name=user.name,
        role=user.role,
    )


@router.post("/logout")
@inject
async def logout(
    response: fastapi.Response,
    service: AuthService = fastapi.Depends(
        Provide[ApplicationContainer.services.auth]
    ),
) -> None:
    return await service.logout(response=response)
