"""
学院API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成。

约定：
- HTTP 层统一只依赖 Service，不直接依赖 Repository。
- 字段校验由 Schema 在进入端点前完成。
"""

from fastapi import APIRouter, Depends, Path, Query, status

from core.dependencies import get_sys_college_service
from service.sys_college_service import SysCollegeService
from schemas.sys_college import (
    SysCollegeCreate,
    SysCollegeUpdate,
    SysCollegeResponse,
    
)
from schemas.response import (
    SuccessResponse,
    PaginationResponse,
    success_response,
    paginated_response,
)
from utils.custom_exceptions import handle_service_exceptions


router = APIRouter(prefix="/sys-college", tags=["学院管理"])


@router.get(
    "",
    response_model=PaginationResponse[SysCollegeResponse],
    status_code=status.HTTP_200_OK,
    summary="获取学院列表",
)
@handle_service_exceptions
async def get_sys_college_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: SysCollegeService = Depends(get_sys_college_service),
):
    """获取学院分页列表"""
    result = await service.get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size,
    )


@router.get(
    "/{college_id}",
    response_model=SuccessResponse[SysCollegeResponse],
    status_code=status.HTTP_200_OK,
    summary="获取学院详情",
)
@handle_service_exceptions
async def get_sys_college_detail(
    college_id: str = Path(..., description="学院ID编码--业务主键"),
    service: SysCollegeService = Depends(get_sys_college_service),
):
    """获取学院详情"""
    result = await service.get_detail(college_id)
    return success_response(result)


@router.post(
    "",
    response_model=SuccessResponse[SysCollegeResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建学院",
)
@handle_service_exceptions
async def create_sys_college(
    data: SysCollegeCreate,
    service: SysCollegeService = Depends(get_sys_college_service),
):
    """创建学院"""
    result = await service.create(data)
    return success_response(result, message="学院创建成功")


@router.put(
    "/{college_id}",
    response_model=SuccessResponse[SysCollegeResponse],
    summary="更新学院",
)
@handle_service_exceptions
async def update_sys_college(
    college_id: str = Path(..., description="学院ID编码--业务主键"),
    data: SysCollegeUpdate = ...,
    service: SysCollegeService = Depends(get_sys_college_service),
):
    """更新学院（不含状态/标识位字段）"""
    result = await service.update(college_id, data)
    return success_response(result, message="学院更新成功")





@router.delete(
    "/{college_id}",
    response_model=SuccessResponse[None],
    summary="删除学院",
)
@handle_service_exceptions
async def delete_sys_college(
    college_id: str = Path(..., description="学院ID编码--业务主键"),
    service: SysCollegeService = Depends(get_sys_college_service),
):
    """删除学院"""
    await service.delete(college_id)
    return success_response(None, message="学院删除成功")