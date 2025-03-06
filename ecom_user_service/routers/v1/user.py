import fastapi
from dependency_injector.wiring import inject, Provide

from ecom_user_service.containers.application import ApplicationContainer
from ecom_user_service.models import User
from ecom_user_service.schemas.user import UserReadSchema, UserPatchSchema
from ecom_user_service.security import Security
from ecom_user_service.services.user import UserService

router = fastapi.APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/me")
async def get_me(
    user: User = fastapi.Depends(Security())
) -> UserReadSchema:
    return UserReadSchema.model_validate(user)


@router.patch("/")
@inject
async def patch_me(
    patch_data: UserPatchSchema,
    user: User = fastapi.Depends(Security()),
    service: UserService = fastapi.Depends(
        Provide[ApplicationContainer.services.user]
    )
) -> UserReadSchema:
    return await service.patch_user(
        user_id=user.id,
        new_name=patch_data.name,
        new_age=patch_data.age,
    )
