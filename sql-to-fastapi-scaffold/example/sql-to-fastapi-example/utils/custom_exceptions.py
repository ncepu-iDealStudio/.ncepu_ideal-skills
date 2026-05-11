"""
自定义异常模块

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Optional, Callable
import traceback


class BaseException(Exception):
    def __init__(self, message: str, code: str = "ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class BadRequestException(BaseException):
    def __init__(self, message: str = "请求参数错误"):
        super().__init__(message, code="BAD_REQUEST")
        self.status_code = status.HTTP_400_BAD_REQUEST


class NotFoundException(BaseException):
    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, code="NOT_FOUND")
        self.status_code = status.HTTP_404_NOT_FOUND


class UnauthorizedException(BaseException):
    def __init__(self, message: str = "未授权"):
        super().__init__(message, code="UNAUTHORIZED")
        self.status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenException(BaseException):
    def __init__(self, message: str = "禁止访问"):
        super().__init__(message, code="FORBIDDEN")
        self.status_code = status.HTTP_403_FORBIDDEN


class InternalServerError(BaseException):
    def __init__(self, message: str = "服务器内部错误"):
        super().__init__(message, code="INTERNAL_SERVER_ERROR")
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


async def handle_service_exceptions(request: Request, call_next: Callable):
    try:
        response = await call_next(request)
        return response
    except BadRequestException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "code": e.code,
                "message": e.message,
                "data": None
            }
        )
    except NotFoundException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "code": e.code,
                "message": e.message,
                "data": None
            }
        )
    except UnauthorizedException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "code": e.code,
                "message": e.message,
                "data": None
            }
        )
    except ForbiddenException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "code": e.code,
                "message": e.message,
                "data": None
            }
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": "INTERNAL_SERVER_ERROR",
                "message": "服务器内部错误",
                "data": None
            }
        )