import uuid

import pydantic

from ecom_user_service.enums import UserTypeEnum
from .base import BaseSchema


class UserCreateSchema(BaseSchema):
    email: str
    password: pydantic.SecretStr
    age: int = pydantic.Field(gt=0)
    name: str
    role: UserTypeEnum


class UserReadSchema(BaseSchema):
    id: uuid.UUID
    email: str
    age: int = pydantic.Field(gt=0)
    name: str
    role: UserTypeEnum
