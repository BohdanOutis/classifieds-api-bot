import os
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool


from src.api.main import app
from src.core.database import get_async_session
from src.models.base import Base
from src.core.security import verify_api_key

TEST_DB_PASSWORD = os.getenv("TEST__DB_PASSWORD")
TEST_DB_NAME = os.getenv("TEST__DB_NAME")

TEST_DATABASE_URL = f"postgresql+asyncpg://postgres:{TEST_DB_PASSWORD}@localhost:5432/{TEST_DB_NAME}"

test_engine = create_async_engine(
    TEST_DATABASE_URL, 
    poolclass=NullPool,
    echo=False, 
    future=True
)
test_async_session_maker = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)

async def override_get_async_session() -> AsyncSession:
    async with test_async_session_maker() as session:
        yield session

# Підміняємо залежність бази даних на тестову
app.dependency_overrides[get_async_session] = override_get_async_session

@pytest.fixture(autouse=True)
async def setup_database():
    """Створює чисту базу даних перед кожним тестом і видаляє після."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client():
    """Асинхронний HTTP-клієнт для запитів до FastAPI."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

async def override_verify_api_key():
    return True

app.dependency_overrides[verify_api_key] = override_verify_api_key