import datetime
import uuid

import bcrypt
from jose import jwt, JWTError

from ecom_user_service.enums import UserTypeEnum
from ecom_user_service.exceptions.auth import InvalidCredentials, UserAlreadyExists
from ecom_user_service.gateways.db import Database
from ecom_user_service.models.user import User
from ecom_user_service.repositories.user import UserRepository
from ecom_user_service.schemas.auth import TokenSchema


class AuthService:
    db: Database
    user_repository: UserRepository
    access_token_ttl_days: int
    secret_key: str

    def __init__(
        self,
        db: Database,
        user_repository: UserRepository,
        access_token_ttl_days: int,
        secret_key: str
    ):
        self.db = db
        self.user_repository = user_repository
        self.access_token_ttl_days = access_token_ttl_days
        self.secret_key = secret_key

    async def login(
        self, email: str, raw_password: str
    ) -> TokenSchema:
        user = await self.user_repository.get_one_or_none(
            User.email == email,
        )
        if not user:
            raise InvalidCredentials()
        # if not self._verify_password(raw_password, user.hashed_password):
        #     raise InvalidCredentials()

        user_data = {
            "id": str(user.id),
            "role": user.role,
        }
        token = self._create_access_token(user_data)
        return TokenSchema(
            token=token,
            type="Bearer",
        )

    async def register(
        self,
        email: str,
        raw_password: str,
        age: int,
        name: str,
        role: UserTypeEnum,
    ) -> None:
        user = await self.user_repository.get_one_or_none(
            User.email == email,
        )
        if user:
            raise UserAlreadyExists()

        hashed_password = self._hash_password(raw_password)
        user = User(
            id=uuid.uuid4(),
            email=email,
            hashed_password=hashed_password,
            age=age,
            name=name,
            role=role.value,
        )
        await self.user_repository.create(user)

    async def authenticate(self, token: str) -> User:
        try:
            data = jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except JWTError:
            raise InvalidCredentials()
        try:
            user_id = data["id"]
        except KeyError:
            raise InvalidCredentials()
        user = await self.user_repository.get_one_or_none(
            User.id == user_id,
        )
        if not user:
            raise InvalidCredentials()
        return user

    def _create_access_token(self, data: dict) -> str:
        expire = (
            datetime.datetime.now(datetime.UTC) +
            datetime.timedelta(days=self.access_token_ttl_days)
        )
        data.update({"exp": expire})
        return jwt.encode(data, self.secret_key, algorithm="HS256")

    @staticmethod
    def _hash_password(raw_password: str) -> str:
        salt = bcrypt.gensalt()
        bytes_password = bytes(raw_password, encoding="utf-8")
        hashed_password = bcrypt.hashpw(bytes_password, salt)
        return hashed_password.decode()

    @staticmethod
    def _verify_password(raw_password: str, hashed_password: str) -> bool:
        bytes_password = bytes(raw_password, encoding="utf-8")
        bytes_hashed_password = bytes(hashed_password, encoding="utf-8")
        return bcrypt.checkpw(bytes_password, bytes_hashed_password)
