import pytest_asyncio
from typing import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.main import app
from app.core.database import settings, Base

TEST_DATABASE_URL = settings.DATABASE_URL.replace("app_db", "app_db") # Using same DB for now

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()
        await session.close()
    
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
