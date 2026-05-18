"""API v1路由包

此文件由 SQL-to-FastAPI-Scaffold 自动生成

注册v1版本下的所有子路由并导出
"""

from fastapi import APIRouter

from api.v1.{{first_resource}} import router as {{class_name}}Router

v1_router = APIRouter()

v1_router.include_router({{class_name}}Router)

{% for resource in other_resources %}
from api.v1.{{resource.file_name}} import router as {{resource.class_name}}Router
v1_router.include_router({{resource.class_name}}Router)
{% endfor %}

__all__ = ["v1_router"]
