import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, declared_attr


class BaseModel(DeclarativeBase):
    metadata = sa.MetaData(schema="public")

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    def __repr__(self) -> str:
        attrs = ', '.join(f"{key}={value!r}" for key, value in self.__dict__.items())
        return f"<{self.__class__.__name__}>({attrs})"
