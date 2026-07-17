"""
班级信息（classinfo）API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成。

约定：
- HTTP 层统一只依赖 Service，不直接依赖 Repository。
- 字段校验由 Schema 在进入端点前完成。
"""

from fastapi import APIRouter, Depends, Path, Query, status

from core.dependencies import get_sys_classinfo_service
from service.sys_classinfo_service import SysClassinfoService
from schemas.sys_classinfo import (
    SysClassinfoCreate,
    SysClassinfoUpdate,
    SysClassinfoResponse,
    
)
from schemas.response import (
    SuccessResponse,
    PaginationResponse,
    success_response,
    paginated_response,
)
from utils.custom_exceptions import handle_service_exceptions


router = APIRouter(prefix="/sys-classinfo", tags=["班级信息（classinfo）管理"])


@router.get(
    "",
    response_model=PaginationResponse[SysClassinfoResponse],
    status_code=status.HTTP_200_OK,
    summary="获取班级信息（classinfo）列表",
)
@handle_service_exceptions
async def get_sys_classinfo_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: SysClassinfoService = Depends(get_sys_classinfo_service),
):
    """获取班级信息（classinfo）分页列表"""
    result = await service.get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size,
    )


@router.get(
    "/{auto_id}",
    response_model=SuccessResponse[SysClassinfoResponse],
    status_code=status.HTTP_200_OK,
    summary="获取班级信息（classinfo）详情",
)
@handle_service_exceptions
async def get_sys_classinfo_detail(
    auto_id: int = Path(..., description="自增主键"),
    service: SysClassinfoService = Depends(get_sys_classinfo_service),
):
    """获取班级信息（classinfo）详情"""
    result = await service.get_detail(auto_id)
    return success_response(result)


@router.post(
    "",
    response_model=SuccessResponse[SysClassinfoResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建班级信息（classinfo）",
)
@handle_service_exceptions
async def create_sys_classinfo(
    data: SysClassinfoCreate,
    service: SysClassinfoService = Depends(get_sys_classinfo_service),
):
    """创建班级信息（classinfo）"""
    result = await service.create(data)
    return success_response(result, message="班级信息（classinfo）创建成功")


@router.put(
    "/{auto_id}",
    response_model=SuccessResponse[SysClassinfoResponse],
    summary="更新班级信息（classinfo）",
)
@handle_service_exceptions
async def update_sys_classinfo(
    auto_id: int = Path(..., description="自增主键"),
    data: SysClassinfoUpdate = ...,
    service: SysClassinfoService = Depends(get_sys_classinfo_service),
):
    """更新班级信息（classinfo）（不含状态/标识位字段）"""
    result = await service.update(auto_id, data)
    return success_response(result, message="班级信息（classinfo）更新成功")





@router.delete(
    "/{auto_id}",
    response_model=SuccessResponse[None],
    summary="删除班级信息（classinfo）",
)
@handle_service_exceptions
async def delete_sys_classinfo(
    auto_id: int = Path(..., description="自增主键"),
    service: SysClassinfoService = Depends(get_sys_classinfo_service),
):
    """删除班级信息（classinfo）"""
    await service.delete(auto_id)
    return success_response(None, message="班级信息（classinfo）删除成功")