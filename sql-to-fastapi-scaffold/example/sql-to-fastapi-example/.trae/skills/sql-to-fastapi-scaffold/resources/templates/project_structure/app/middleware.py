"""中间件配置

此文件由 SQL-to-FastAPI-Scaffold 自动生成

直接在app层注册中间件
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings


def setup(app: FastAPI) -> None:
    """
    注册所有中间件

    Args:
        app: FastAPI应用实例
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
