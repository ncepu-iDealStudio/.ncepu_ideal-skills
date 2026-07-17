"""
用户账号信息（登录中心）API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成。

约定：
- HTTP 层统一只依赖 Service，不直接依赖 Repository。
- 字段校验由 Schema 在进入端点前完成。
- 状态/标识位字段通过 PATCH /{auto_id}/status 专用修改。
"""

from fastapi import APIRouter, Depends, Path, Query, status

from core.dependencies import get_sso_user_service
from service.sso_user_service import SsoUserService
from schemas.sso_user import (
    SsoUserCreate,
    SsoUserUpdate,
    SsoUserResponse,
    
    SsoUserStatusUpdate,
    
)
from schemas.response import (
    SuccessResponse,
    PaginationResponse,
    success_response,
    paginated_response,
)
from utils.custom_exceptions import handle_service_exceptions


router = APIRouter(prefix="/sso-user", tags=["用户账号信息（登录中心）管理"])


@router.get(
    "",
    response_model=PaginationResponse[SsoUserResponse],
    status_code=status.HTTP_200_OK,
    summary="获取用户账号信息（登录中心）列表",
)
@handle_service_exceptions
async def get_sso_user_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: SsoUserService = Depends(get_sso_user_service),
):
    """获取用户账号信息（登录中心）分页列表"""
    result = await service.get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size,
    )


@router.get(
    "/{auto_id}",
    response_model=SuccessResponse[SsoUserResponse],
    status_code=status.HTTP_200_OK,
    summary="获取用户账号信息（登录中心）详情",
)
@handle_service_exceptions
async def get_sso_user_detail(
    auto_id: int = Path(..., description="物理主键，自增"),
    service: SsoUserService = Depends(get_sso_user_service),
):
    """获取用户账号信息（登录中心）详情"""
    result = await service.get_detail(auto_id)
    return success_response(result)


@router.post(
    "",
    response_model=SuccessResponse[SsoUserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建用户账号信息（登录中心）",
)
@handle_service_exceptions
async def create_sso_user(
    data: SsoUserCreate,
    service: SsoUserService = Depends(get_sso_user_service),
):
    """创建用户账号信息（登录中心）"""
    result = await service.create(data)
    return success_response(result, message="用户账号信息（登录中心）创建成功")


@router.put(
    "/{auto_id}",
    response_model=SuccessResponse[SsoUserResponse],
    summary="更新用户账号信息（登录中心）",
)
@handle_service_exceptions
async def update_sso_user(
    auto_id: int = Path(..., description="物理主键，自增"),
    data: SsoUserUpdate = ...,
    service: SsoUserService = Depends(get_sso_user_service),
):
    """更新用户账号信息（登录中心）（不含状态/标识位字段）"""
    result = await service.update(auto_id, data)
    return success_response(result, message="用户账号信息（登录中心）更新成功")



@router.patch(
    "/{auto_id}/status",
    response_model=SuccessResponse[SsoUserResponse],
    summary="修改用户账号信息（登录中心）状态/标识位",
)
@handle_service_exceptions
async def update_sso_user_status(
    auto_id: int = Path(..., description="物理主键，自增"),
    data: SsoUserStatusUpdate = ...,
    service: SsoUserService = Depends(get_sso_user_service),
):
    """
    专用修改状态/标识位：status
    """
    result = await service.update_status(auto_id, data)
    return success_response(result, message="用户账号信息（登录中心）状态更新成功")



@router.delete(
    "/{auto_id}",
    response_model=SuccessResponse[None],
    summary="删除用户账号信息（登录中心）",
)
@handle_service_exceptions
async def delete_sso_user(
    auto_id: int = Path(..., description="物理主键，自增"),
    service: SsoUserService = Depends(get_sso_user_service),
):
    """删除用户账号信息（登录中心）"""
    await service.delete(auto_id)
    return success_response(None, message="用户账号信息（登录中心）删除成功")