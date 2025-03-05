import pydantic

from .base import BaseSchema


class TokenSchema(BaseSchema):
    type_: str = pydantic.Field(alias="type")
    token: str


class LoginSchema(BaseSchema):
    email: str
    raw_password: pydantic.SecretStr
