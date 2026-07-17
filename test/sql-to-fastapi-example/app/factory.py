"""应用工厂函数

此文件由 SQL-to-FastAPI-Scaffold 自动生成

创建和配置FastAPI应用实例
"""

from fastapi import FastAPI
from loguru import logger

from config import settings
from utils.loguru import setup_logging
from .events import lifespan_manager
from .middleware import setup as register_middlewares
from .exceptions import setup_exception_handlers
from .router import register_routes


def create_app() -> FastAPI:
    """
    创建并配置FastAPI应用实例

    Returns:
        FastAPI: 配置完成的FastAPI应用实例
    """
    setup_logging()
    logger.info("📦 开始创建FastAPI应用实例...")

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        lifespan=lifespan_manager
    )

    logger.info("🔧 正在注册中间件...")
    register_middlewares(app)
    logger.info("✅ 中间件注册完成")

    logger.info("🔧 正在注册异常处理器...")
    setup_exception_handlers(app)
    logger.info("✅ 异常处理器注册完成")

    logger.info("🔧 正在注册路由...")
    register_routes(app)
    logger.info("✅ 路由注册完成")

    logger.info(f"🎉 FastAPI应用创建成功 - {settings.APP_NAME} v{settings.APP_VERSION}")

    return app
