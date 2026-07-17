"""
班级信息API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成。

约定：
- HTTP 层统一只依赖 Service，不直接依赖 Repository。
- 字段校验由 Schema 在进入端点前完成。
"""

from fastapi import APIRouter, Depends, Path, Query, status

from core.dependencies import get_sys_class_service
from service.sys_class_service import SysClassService
from schemas.sys_class import (
    SysClassCreate,
    SysClassUpdate,
    SysClassResponse,
    
)
from schemas.response import (
    SuccessResponse,
    PaginationResponse,
    success_response,
    paginated_response,
)
from utils.custom_exceptions import handle_service_exceptions


router = APIRouter(prefix="/sys-class", tags=["班级信息管理"])


@router.get(
    "",
    response_model=PaginationResponse[SysClassResponse],
    status_code=status.HTTP_200_OK,
    summary="获取班级信息列表",
)
@handle_service_exceptions
async def get_sys_class_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: SysClassService = Depends(get_sys_class_service),
):
    """获取班级信息分页列表"""
    result = await service.get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size,
    )


@router.get(
    "/{class_id}",
    response_model=SuccessResponse[SysClassResponse],
    status_code=status.HTTP_200_OK,
    summary="获取班级信息详情",
)
@handle_service_exceptions
async def get_sys_class_detail(
    class_id: str = Path(..., description="班级ID--业务主键"),
    service: SysClassService = Depends(get_sys_class_service),
):
    """获取班级信息详情"""
    result = await service.get_detail(class_id)
    return success_response(result)


@router.post(
    "",
    response_model=SuccessResponse[SysClassResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建班级信息",
)
@handle_service_exceptions
async def create_sys_class(
    data: SysClassCreate,
    service: SysClassService = Depends(get_sys_class_service),
):
    """创建班级信息"""
    result = await service.create(data)
    return success_response(result, message="班级信息创建成功")


@router.put(
    "/{class_id}",
    response_model=SuccessResponse[SysClassResponse],
    summary="更新班级信息",
)
@handle_service_exceptions
async def update_sys_class(
    class_id: str = Path(..., description="班级ID--业务主键"),
    data: SysClassUpdate = ...,
    service: SysClassService = Depends(get_sys_class_service),
):
    """更新班级信息（不含状态/标识位字段）"""
    result = await service.update(class_id, data)
    return success_response(result, message="班级信息更新成功")





@router.delete(
    "/{class_id}",
    response_model=SuccessResponse[None],
    summary="删除班级信息",
)
@handle_service_exceptions
async def delete_sys_class(
    class_id: str = Path(..., description="班级ID--业务主键"),
    service: SysClassService = Depends(get_sys_class_service),
):
    """删除班级信息"""
    await service.delete(class_id)
    return success_response(None, message="班级信息删除成功")