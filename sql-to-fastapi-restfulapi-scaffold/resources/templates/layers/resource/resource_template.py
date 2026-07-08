"""
{{table_comment}}API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, status

from core.dependencies import get_{{service_name}}
from schemas.{{table_name}} import (
    {{class_name}}Create,
    {{class_name}}Update,
    {{class_name}}Response
)
from schemas.response import SuccessResponse, PaginationResponse, success_response, paginated_response


router = APIRouter(prefix="/{{resource_singular}}", tags=["{{table_comment}}管理"])


@router.get(
    "",
    response_model=PaginationResponse[{{class_name}}Response],
    status_code=status.HTTP_200_OK,
    summary="获取{{table_comment}}记录列表",
    description="分页获取{{table_comment}}记录列表，支持多种筛选条件"
)
async def get_{{resource_singular}}_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: {{class_name}}Service = Depends(get_{{service_name}})
):
    """
    获取{{table_comment}}记录列表
    """
    result = service.get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size
    )


@router.get(
    "/{{primary_key_param}}",
    response_model=SuccessResponse[{{class_name}}Response],
    status_code=status.HTTP_200_OK,
    summary="获取{{table_comment}}记录详细信息"
)
async def get_{{resource_singular}}_detail(
    {{primary_key_param}}: {{primary_key_type}} = Path(..., description="{{primary_key_comment}}"),
    service: {{class_name}}Service = Depends(get_{{service_name}})
):
    """
    获取{{table_comment}}记录详细信息
    """
    result = service.get_detail({{primary_key_param}})
    return success_response(result)


@router.post(
    "",
    response_model=SuccessResponse[{{class_name}}Response],
    status_code=status.HTTP_201_CREATED,
    summary="创建{{table_comment}}记录"
)
async def create_{{resource_singular}}(
    data: {{class_name}}Create,
    service: {{class_name}}Service = Depends(get_{{service_name}})
):
    """
    创建{{table_comment}}记录
    """
    result = service.create(data)
    return success_response(result, message="{{table_comment}}记录创建成功")


@router.put(
    "/{{primary_key_param}}",
    response_model=SuccessResponse[{{class_name}}Response],
    summary="更新{{table_comment}}记录信息"
)
async def update_{{resource_singular}}(
    {{primary_key_param}}: {{primary_key_type}} = Path(..., description="{{primary_key_comment}}"),
    data: {{class_name}}Update = ...,
    service: {{class_name}}Service = Depends(get_{{service_name}})
):
    """
    更新{{table_comment}}记录信息
    """
    result = service.update({{primary_key_param}}, data)
    return success_response(result, message="{{table_comment}}记录更新成功")


@router.delete(
    "/{{primary_key_param}}",
    response_model=SuccessResponse[None],
    summary="删除{{table_comment}}记录"
)
async def delete_{{resource_singular}}(
    {{primary_key_param}}: {{primary_key_type}} = Path(..., description="{{primary_key_comment}}"),
    service: {{class_name}}Service = Depends(get_{{service_name}})
):
    """
    删除{{table_comment}}记录
    """
    service.delete({{primary_key_param}})
    return success_response(None, message="{{table_comment}}记录删除成功")
