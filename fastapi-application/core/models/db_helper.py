from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from core.config import settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,  # Отключает автоматическую отправку изменений в БД перед запросами. Без autoflush можно накопить несколько изменений и отправить одним запросом
            autocommit=False,  # Запрещает автоматическое коммитление после каждого запроса. Требует явного вызова commit() или rollback()
            expire_on_commit=False,  # Не сбрасывает состояние объектов после коммита. Позволяет повторно использовать объекты без повторного запроса к БД.
        )

    async def dispose(self) -> None:
        await self.engine.dispose()  # асинхронно закрывает все соединения в пуле

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:  # Асинхронный контекстный менеджер для работы с сессиями
            yield session
            # await session.close() - уже реализовано. Произойдёт автоматически.


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
