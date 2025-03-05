from ecom_user_service.gateways.db import Database
from ecom_user_service.models.user import User
from ecom_user_service.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self, db: Database):
        super().__init__(User, db)
