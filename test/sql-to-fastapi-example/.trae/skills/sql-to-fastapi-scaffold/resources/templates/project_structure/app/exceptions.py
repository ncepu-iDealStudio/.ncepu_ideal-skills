"""异常处理器配置

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from utils.custom_exceptions import BaseException
from schemas.response import ErrorResponse


def setup_exception_handlers(app: FastAPI) -> None:
    """
    设置异常处理器

    Args:
        app: FastAPI应用实例
    """

    @app.exception_handler(BaseException)
    async def api_exception_handler(request: Request, exc: BaseException):
        """处理自定义API异常"""
        error_response = ErrorResponse(exc.code, exc.message)
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump()
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """处理请求验证异常"""
        errors = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"][1:])
            errors.append({"field": field, "message": error["msg"]})

        return JSONResponse(
            status_code=422,
            content={
                "code": "VALIDATION_ERROR",
                "message": "请求参数验证失败",
                "errors": errors
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """处理HTTP异常"""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": "HTTP_ERROR",
                "message": exc.detail
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """处理未捕获的异常"""
        return JSONResponse(
            status_code=500,
            content={
                "code": "INTERNAL_SERVER_ERROR",
                "message": "服务器内部错误"
            }
        )
