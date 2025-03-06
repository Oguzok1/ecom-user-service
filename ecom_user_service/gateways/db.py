from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class Database:
    _factory: async_sessionmaker[AsyncSession]

    def __init__(
        self,
        url: str
    ):
        engine = create_async_engine(url, echo=True,)
        self._factory = async_sessionmaker(engine, expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self, session: AsyncSession | None = None) -> AsyncGenerator[AsyncSession, None]:
        if session is not None:
            yield session
        else:
            async with self._factory() as session:
                yield session
