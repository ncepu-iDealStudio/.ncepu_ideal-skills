"""
管理员API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成。

约定：
- HTTP 层统一只依赖 Service，不直接依赖 Repository。
- 字段校验由 Schema 在进入端点前完成。
"""

from fastapi import APIRouter, Depends, Path, Query, status

from core.dependencies import get_admin_service
from service.admin_service import AdminService
from schemas.admin import (
    AdminCreate,
    AdminUpdate,
    AdminResponse,
    
)
from schemas.response import (
    SuccessResponse,
    PaginationResponse,
    success_response,
    paginated_response,
)
from utils.custom_exceptions import handle_service_exceptions


router = APIRouter(prefix="/admin", tags=["管理员管理"])


@router.get(
    "",
    response_model=PaginationResponse[AdminResponse],
    status_code=status.HTTP_200_OK,
    summary="获取管理员列表",
)
@handle_service_exceptions
async def get_admin_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: AdminService = Depends(get_admin_service),
):
    """获取管理员分页列表"""
    result = await service.get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size,
    )


@router.get(
    "/{auto_id}",
    response_model=SuccessResponse[AdminResponse],
    status_code=status.HTTP_200_OK,
    summary="获取管理员详情",
)
@handle_service_exceptions
async def get_admin_detail(
    auto_id: int = Path(..., description="自增主键"),
    service: AdminService = Depends(get_admin_service),
):
    """获取管理员详情"""
    result = await service.get_detail(auto_id)
    return success_response(result)


@router.post(
    "",
    response_model=SuccessResponse[AdminResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建管理员",
)
@handle_service_exceptions
async def create_admin(
    data: AdminCreate,
    service: AdminService = Depends(get_admin_service),
):
    """创建管理员"""
    result = await service.create(data)
    return success_response(result, message="管理员创建成功")


@router.put(
    "/{auto_id}",
    response_model=SuccessResponse[AdminResponse],
    summary="更新管理员",
)
@handle_service_exceptions
async def update_admin(
    auto_id: int = Path(..., description="自增主键"),
    data: AdminUpdate = ...,
    service: AdminService = Depends(get_admin_service),
):
    """更新管理员（不含状态/标识位字段）"""
    result = await service.update(auto_id, data)
    return success_response(result, message="管理员更新成功")





@router.delete(
    "/{auto_id}",
    response_model=SuccessResponse[None],
    summary="删除管理员",
)
@handle_service_exceptions
async def delete_admin(
    auto_id: int = Path(..., description="自增主键"),
    service: AdminService = Depends(get_admin_service),
):
    """删除管理员"""
    await service.delete(auto_id)
    return success_response(None, message="管理员删除成功")