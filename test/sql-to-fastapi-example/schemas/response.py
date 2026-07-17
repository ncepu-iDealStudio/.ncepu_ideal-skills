"""
统一响应模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Generic, TypeVar, List, Optional, Any
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


T = TypeVar("T")


class BaseResponse(BaseModel):
    """
    基础响应模型
    """
    code: str = "SUCCESS"
    message: str = "操作成功"
    timestamp: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)


class SuccessResponse(BaseResponse, Generic[T]):
    """
    统一成功响应模型
    """
    data: Optional[T] = None

    @classmethod
    def success(cls, data: T, message: str = "操作成功"):
        """
        创建成功响应
        """
        return cls(code="SUCCESS", message=message, data=data)


class PaginationResponse(BaseResponse, Generic[T]):
    """
    分页响应模型
    """
    data: dict

    @classmethod
    def paginated(
        cls,
        items: List[T],
        total: int,
        page: int,
        size: int
    ):
        """
        创建分页响应
        """
        return cls(
            code="SUCCESS",
            message="操作成功",
            data={
                "items": items,
                "total": total,
                "page": page,
                "size": size,
                "pages": (total + size - 1) // size if size > 0 else 0
            }
        )


class ErrorResponse(BaseResponse):
    """
    统一错误响应模型
    """
    code: str = "ERROR"
    message: str = "操作失败"
    data: Optional[Any] = None

    @classmethod
    def error(cls, code: str, message: str, data: Any = None):
        """
        创建错误响应
        """
        return cls(code=code, message=message, data=data)


def success_response(data, message: str = "操作成功"):
    """
    返回成功响应的辅助函数
    """
    return SuccessResponse.success(data=data, message=message)


def paginated_response(items: List[T], total: int, page: int, size: int):
    """
    返回分页响应的辅助函数
    """
    return PaginationResponse.paginated(items=items, total=total, page=page, size=size)
