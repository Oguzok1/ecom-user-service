import uuid

from ecom_user_service.gateways.db import Database
from ecom_user_service.models import User
from ecom_user_service.repositories.user import UserRepository
from ecom_user_service.schemas.user import UserReadSchema


class UserService:
    db: Database
    user_repository: UserRepository

    def __init__(
        self,
        db: Database,
        user_repository: UserRepository
    ):
        self.db = db
        self.user_repository = user_repository

    async def patch_user(
        self,
        user_id: uuid.UUID,
        new_name: str | None = None,
        new_age: int | None = None,
    ) -> UserReadSchema:
        update = {}
        if new_name is not None:
            update["name"] = new_name
        if new_age is not None:
            update["age"] = new_age
        user = await self.user_repository.update(
            User.id == user_id,
            **update
        )
        print(f"{user.name=}")
        return UserReadSchema.model_validate(user, from_attributes=True)
