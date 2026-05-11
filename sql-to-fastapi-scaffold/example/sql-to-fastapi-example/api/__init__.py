"""API路由包

此文件由 SQL-to-FastAPI-Scaffold 自动生成

导出各版本路由
"""

from fastapi import APIRouter

from . import v1

api_router = APIRouter()

api_router.include_router(v1.v1_router, prefix="/v1", tags=["v1"])

__all__ = ["api_router"]