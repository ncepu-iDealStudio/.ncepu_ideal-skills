"""模型基类

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from core.database import Base


class BaseModel(Base):
    """ORM 抽象基类：所有业务模型继承此类"""

    __abstract__ = True
