"""
自定义异常模块

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Callable

from fastapi import status


class BaseException(Exception):
    """
    基础异常类
    """
    def __init__(self, message: str, code: str = "ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class BadRequestException(BaseException):
    """
    400 - 请求参数错误
    """
    def __init__(self, message: str = "请求参数错误"):
        super().__init__(message, code="BAD_REQUEST")
        self.status_code = status.HTTP_400_BAD_REQUEST


class NotFoundException(BaseException):
    """
    404 - 资源不存在
    """
    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, code="NOT_FOUND")
        self.status_code = status.HTTP_404_NOT_FOUND


class UnauthorizedException(BaseException):
    """
    401 - 未授权
    """
    def __init__(self, message: str = "未授权"):
        super().__init__(message, code="UNAUTHORIZED")
        self.status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenException(BaseException):
    """
    403 - 禁止访问
    """
    def __init__(self, message: str = "禁止访问"):
        super().__init__(message, code="FORBIDDEN")
        self.status_code = status.HTTP_403_FORBIDDEN


class InternalServerError(BaseException):
    """
    500 - 服务器内部错误
    """
    def __init__(self, message: str = "服务器内部错误"):
        super().__init__(message, code="INTERNAL_SERVER_ERROR")
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


def handle_service_exceptions(func: Callable):
    """路由装饰器：业务异常向上抛出，由全局异常处理器统一响应。

    未知异常包装为 InternalServerError 再抛出。
    """
    from functools import wraps
    import inspect

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except BaseException:
            raise
        except Exception as e:
            raise InternalServerError(f"服务异常: {e}") from e

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException:
            raise
        except Exception as e:
            raise InternalServerError(f"服务异常: {e}") from e

    if inspect.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper
