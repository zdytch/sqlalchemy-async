from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import UUID as UUIDField
from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import (
    AsyncSession as DB,
    create_async_engine,
    async_sessionmaker,
)
from uuid import UUID, uuid4
import os

DB_URL = (
    f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:'
    f'{os.getenv("POSTGRES_PASSWORD")}@'
    f'{os.getenv("POSTGRES_HOSTNAME")}:'
    f'{os.getenv("POSTGRES_PORT")}/'
    f'{os.getenv("POSTGRES_DATABASE")}'
)

_engine = create_async_engine(DB_URL, connect_args={'server_settings': {'jit': 'off'}})

Session = async_sessionmaker(_engine, class_=DB, expire_on_commit=False)


class Model(DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(UUIDField, default=uuid4, primary_key=True)

    @declared_attr  # type: ignore
    def __tablename__(cls):
        return cls.__name__.lower()

    def __hash__(self):
        return hash(self.id)


async def get_db():
    async with Session() as session:
        yield session


async def create_all_tables():
    async with _engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def drop_all_tables():
    async with _engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
