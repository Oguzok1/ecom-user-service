import uuid

from sqlalchemy.orm import Mapped, mapped_column

from ecom_user_service.models import BaseModel


class User(BaseModel):
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    age: Mapped[int]
    hashed_password: Mapped[str]
    role: Mapped[str]
