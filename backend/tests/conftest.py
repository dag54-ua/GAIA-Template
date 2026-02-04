import pytest_asyncio
from typing import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.main import app
from app.core.database import settings, Base

TEST_DATABASE_URL = settings.DATABASE_URL.replace("app_db", "app_db") # Using same DB for now

from sqlalchemy.pool import NullPool

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    # Re-create engine per test to ensure fresh loop association if pytest-asyncio switches loops
    engine = create_async_engine(TEST_DATABASE_URL, echo=True, poolclass=NullPool)
    
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
        await session.rollback()
    
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    # Use ASGITransport but ensure app is clean.
    # The error suggests the app's internal state (DB connection?) is bound to a different loop.
    # We are mocking the DB dependency in the test? No, we use `db_session`.
    # Let's override the dependency.
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
