"""
依赖注入容器

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from sqlalchemy.orm import Session
from fastapi import Depends
from core.database import get_db


{% for service in services %}
def get_{{service.service_name}}(db: Session = Depends(get_db)) -> {{service.class_name}}Service:
    """
    获取{{service.comment}}服务实例
    """
    from service.{{service.file_name}} import {{service.class_name}}Service
    return {{service.class_name}}Service(db)
{% endfor %}

