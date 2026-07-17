"""pytest fixtures

- session: sqlite 内存库（单元测试）
- app: 真实 MySQL 应用（集成测试，依赖 .env DATABASE_URL）
"""

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app import create_app
from core.database import Base, create_database_pool, close_database_pool
from models.base import BaseModel  # noqa: F401 — 确保模型注册


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    Session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as s:
        yield s
    await engine.dispose()


@pytest_asyncio.fixture
async def app():
    application = create_app()
    await create_database_pool()
    yield application
    await close_database_pool()
