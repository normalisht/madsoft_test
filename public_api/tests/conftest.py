import asyncio
import datetime as dt
from uuid import uuid4

from fastapi.encoders import jsonable_encoder
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from public_api.core.db import Base, get_async_session
from public_api.crud import meme_repository
from public_api.main import app
from public_api.schemas.memes import MemeCreate, MemeRead

SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///test.db'

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(init_models())
finally:
    loop.close()
    asyncio.set_event_loop(None)


async def override_get_async_session() -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture
async def session() -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as ac:
        yield ac


@pytest.fixture
async def create_test_meme(session: AsyncSession) -> MemeRead:
    filename = uuid4().hex
    meme_data = MemeCreate(
        description='Test Meme',
        image_url=f'http://test/{filename}',
        filename=filename,
        expires_at=dt.datetime.now() + dt.timedelta(days=1),
    )
    meme = await meme_repository.create(meme_data, session)
    return MemeRead(**jsonable_encoder(meme))
