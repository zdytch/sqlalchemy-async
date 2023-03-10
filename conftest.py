import pytest
import asyncio
import db_config


@pytest.fixture()
async def db():
    async with db_config.Session() as session:
        yield session


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()

    yield loop

    loop.close()


@pytest.fixture(autouse=True)
async def setup_tables():
    await db_config.drop_all_tables()
    await db_config.create_all_tables()

    yield

    await db_config.drop_all_tables()
