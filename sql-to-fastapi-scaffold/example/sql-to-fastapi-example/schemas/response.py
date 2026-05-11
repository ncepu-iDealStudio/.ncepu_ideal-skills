"""
统一响应模型

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Generic, TypeVar, List, Optional, Any
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


T = TypeVar("T")


class BaseResponse(BaseModel):
    code: str = "SUCCESS"
    message: str = "操作成功"
    timestamp: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)


class SuccessResponse(BaseResponse, Generic[T]):
    data: Optional[T] = None

    @classmethod
    def success(cls, data: T, message: str = "操作成功"):
        return cls(code="SUCCESS", message=message, data=data)


class PaginationResponse(BaseResponse, Generic[T]):
    data: dict

    @classmethod
    def paginated(cls, items: List[T], total: int, page: int, size: int):
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
    code: str = "ERROR"
    message: str = "操作失败"
    data: Optional[Any] = None

    @classmethod
    def error(cls, code: str, message: str, data: Any = None):
        return cls(code=code, message=message, data=data)


def success_response(data, message: str = "操作成功"):
    return SuccessResponse.success(data=data, message=message)


def paginated_response(items: List[T], total: int, page: int, size: int):
    return PaginationResponse.paginated(items=items, total=total, page=page, size=size)