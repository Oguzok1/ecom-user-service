import typing

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from ecom_user_service.gateways.db import Database
from ecom_user_service.models import BaseModel

Model = typing.TypeVar("Model", bound=BaseModel)


class BaseRepository[Model]:
    model: Model
    db: Database

    def __init__(
        self,
        model: Model,
        db: Database
    ):
        self.model = model
        self.db = db

    async def get_all(
        self,
        session: AsyncSession | None = None,
        limit: int = 50,
        offset: int = 1,
        *whereclause
    ) -> list[Model]:
        stmt = (
            sa.select(Model)
            .where(*whereclause)
            .limit(limit)
            .offset(offset)
        )
        async with self.db.get_session(session) as session:
            result = await session.execute(stmt)
        return list(result.scalars().all())

    async def get_one_or_none(
        self,
        *whereclause,
        session: AsyncSession | None = None
    ) -> Model | None:
        stmt = (
            sa.select(self.model)
            .where(*whereclause)
        )
        async with self.db.get_session(session) as session:
            result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        model: Model,
        session: AsyncSession | None = None,
    ) -> None:
        session: AsyncSession
        async with self.db.get_session(session) as session:
            session.add(model)
            await session.commit()

    async def update(
        self,
        *whereclause,
        session: AsyncSession | None = None,
        **kwargs
    ) -> Model:
        print(f"{whereclause=}")
        print(f"{session=}")
        print(f"{kwargs=}")
        stmt = (
            sa.update(self.model)
            .where(*whereclause)
            .values(**kwargs)
            .returning(self.model)
        )
        async with self.db.get_session(session) as session:
            result = await session.execute(stmt)
            await session.commit()
        return result.scalar_one()
