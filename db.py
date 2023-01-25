from sqlalchemy.ext.asyncio import AsyncSession as DB, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
import os

DB_URL = (
    f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}:'
    f'{os.getenv("POSTGRES_PASSWORD")}@'
    f'{os.getenv("POSTGRES_HOSTNAME")}:'
    f'{os.getenv("POSTGRES_PORT")}/'
    f'{os.getenv("POSTGRES_DATABASE")}'
)

engine = create_async_engine(DB_URL, connect_args={'server_settings': {'jit': 'off'}})
Session = sessionmaker(engine, class_=DB, expire_on_commit=False)


class DBModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    def __hash__(self):
        return hash(self.id)


async def get_db():
    async with Session() as session:
        yield session


async def create_all():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_all():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
