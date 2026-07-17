"""
数据库连接与会话管理（异步）

此文件由 SQL-to-FastAPI-Scaffold 自动生成。
"""

from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from config.settings import settings

Base = declarative_base()

async_engine: Optional[AsyncEngine] = None
AsyncSessionLocal: Optional[async_sessionmaker[AsyncSession]] = None


def _to_async_url(database_url: str) -> str:
    if database_url.startswith("mysql+pymysql"):
        return database_url.replace("mysql+pymysql", "mysql+aiomysql", 1)
    if database_url.startswith("mysql://"):
        return database_url.replace("mysql://", "mysql+aiomysql://", 1)
    return database_url


async def create_database_pool() -> None:
    """在应用 lifespan 中创建异步连接池"""
    global async_engine, AsyncSessionLocal
    async_url = _to_async_url(settings.DATABASE_URL)
    async_engine = create_async_engine(async_url, pool_pre_ping=False)
    AsyncSessionLocal = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )


async def close_database_pool() -> None:
    global async_engine
    if async_engine is not None:
        await async_engine.dispose()
        async_engine = None


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 依赖：异步数据库会话"""
    if AsyncSessionLocal is None:
        raise RuntimeError("数据库未初始化，请检查应用启动生命周期")
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
