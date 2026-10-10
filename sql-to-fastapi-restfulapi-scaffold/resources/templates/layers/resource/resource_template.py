"""
{{table_comment}}API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成。

约定：
- HTTP 层统一只依赖 Service，不直接依赖 Repository。
- 默认要求登录（get_current_active_user）；公开接口请显式去掉该 Depends。
- 字段校验由 Schema 在进入端点前完成。
{% if status_flag_fields %}- 状态/标识位字段通过 PATCH /{{{primary_key_param}}}/status 专用修改。
{% endif %}"""

from fastapi import APIRouter, Depends, Path, Query, status

from core.permissions import get_current_active_user
from service.dependencies import get_{{service_name}}
from service.{{table_name}}_service import {{class_name}}Service
from schemas.{{table_name}} import (
    {{class_name}}Create,
    {{class_name}}Update,
    {{class_name}}Response,
    {% if status_flag_fields %}
    {{class_name}}StatusUpdate,
    {% endif %}
)
from schemas.response import (
    SuccessResponse,
    PaginationResponse,
    success_response,
    paginated_response,
)
from utils.custom_exceptions import handle_service_exceptions


router = APIRouter(prefix="/{{route_prefix}}", tags=["{{table_comment}}管理"])


@router.get(
    "",
    response_model=PaginationResponse[{{class_name}}Response],
    status_code=status.HTTP_200_OK,
    summary="获取{{table_comment}}列表",
)
@handle_service_exceptions
async def get_{{resource_singular}}_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    _user=Depends(get_current_active_user),
    service: {{class_name}}Service = Depends(get_{{service_name}}),
):
    """获取{{table_comment}}分页列表"""
    result = await service.get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{{{primary_key_param}}}",
    response_model=SuccessResponse[{{class_name}}Response],
    status_code=status.HTTP_200_OK,
    summary="获取{{table_comment}}详情",
)
@handle_service_exceptions
async def get_{{resource_singular}}_detail(
    {{primary_key_param}}: {{primary_key_type}} = Path(..., description="{{primary_key_comment}}"),
    _user=Depends(get_current_active_user),
    service: {{class_name}}Service = Depends(get_{{service_name}}),
):
    """获取{{table_comment}}详情"""
    result = await service.get_detail({{primary_key_param}})
    return success_response(result)


@router.post(
    "",
    response_model=SuccessResponse[{{class_name}}Response],
    status_code=status.HTTP_201_CREATED,
    summary="创建{{table_comment}}",
)
@handle_service_exceptions
async def create_{{resource_singular}}(
    data: {{class_name}}Create,
    _user=Depends(get_current_active_user),
    service: {{class_name}}Service = Depends(get_{{service_name}}),
):
    """创建{{table_comment}}"""
    result = await service.create(data)
    return success_response(result, message="{{table_comment}}创建成功")


@router.put(
    "/{{{primary_key_param}}}",
    response_model=SuccessResponse[{{class_name}}Response],
    summary="更新{{table_comment}}",
)
@handle_service_exceptions
async def update_{{resource_singular}}(
    {{primary_key_param}}: {{primary_key_type}} = Path(..., description="{{primary_key_comment}}"),
    data: {{class_name}}Update = ...,
    _user=Depends(get_current_active_user),
    service: {{class_name}}Service = Depends(get_{{service_name}}),
):
    """更新{{table_comment}}（不含状态/标识位字段）"""
    result = await service.update({{primary_key_param}}, data)
    return success_response(result, message="{{table_comment}}更新成功")


{% if status_flag_fields %}
@router.patch(
    "/{{{primary_key_param}}}/status",
    response_model=SuccessResponse[{{class_name}}Response],
    summary="修改{{table_comment}}状态/标识位",
)
@handle_service_exceptions
async def update_{{resource_singular}}_status(
    {{primary_key_param}}: {{primary_key_type}} = Path(..., description="{{primary_key_comment}}"),
    data: {{class_name}}StatusUpdate = ...,
    _user=Depends(get_current_active_user),
    service: {{class_name}}Service = Depends(get_{{service_name}}),
):
    """
    专用修改状态/标识位：{% for f in status_flag_fields %}{{f.name}}{% if not loop.last %}、{% endif %}{% endfor %}
    """
    result = await service.update_status({{primary_key_param}}, data)
    return success_response(result, message="{{table_comment}}状态更新成功")
{% endif %}


@router.delete(
    "/{{{primary_key_param}}}",
    response_model=SuccessResponse[None],
    summary="删除{{table_comment}}",
)
@handle_service_exceptions
async def delete_{{resource_singular}}(
    {{primary_key_param}}: {{primary_key_type}} = Path(..., description="{{primary_key_comment}}"),
    _user=Depends(get_current_active_user),
    service: {{class_name}}Service = Depends(get_{{service_name}}),
):
    """删除{{table_comment}}"""
    await service.delete({{primary_key_param}})
    return success_response(None, message="{{table_comment}}删除成功")
