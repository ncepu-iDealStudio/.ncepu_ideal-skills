"""应用生命周期管理

此文件由 SQL-to-FastAPI-Scaffold 自动生成

定义应用启动和关闭时的生命周期处理
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from config import settings
from core.database import close_database_pool, create_database_pool


@asynccontextmanager
async def lifespan_manager(app: FastAPI):
    """应用生命周期管理器：启动时初始化异步连接池，关闭时释放。"""
    os.makedirs("logs", exist_ok=True)

    logger.info("🚀 应用正在启动...")
    await create_database_pool()
    logger.info("✅ 数据库连接池初始化完成")
    logger.info(f"🎉 应用启动成功 - {settings.APP_NAME} v{settings.APP_VERSION}")

    yield

    logger.info("🔄 应用正在关闭...")
    await close_database_pool()
    logger.info("👋 应用已安全关闭")
