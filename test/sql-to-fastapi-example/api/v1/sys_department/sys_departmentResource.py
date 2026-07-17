"""
教研室与研究所部门信息API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成。

约定：
- HTTP 层统一只依赖 Service，不直接依赖 Repository。
- 字段校验由 Schema 在进入端点前完成。
"""

from fastapi import APIRouter, Depends, Path, Query, status

from core.dependencies import get_sys_department_service
from service.sys_department_service import SysDepartmentService
from schemas.sys_department import (
    SysDepartmentCreate,
    SysDepartmentUpdate,
    SysDepartmentResponse,
    
)
from schemas.response import (
    SuccessResponse,
    PaginationResponse,
    success_response,
    paginated_response,
)
from utils.custom_exceptions import handle_service_exceptions


router = APIRouter(prefix="/sys-department", tags=["教研室与研究所部门信息管理"])


@router.get(
    "",
    response_model=PaginationResponse[SysDepartmentResponse],
    status_code=status.HTTP_200_OK,
    summary="获取教研室与研究所部门信息列表",
)
@handle_service_exceptions
async def get_sys_department_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: SysDepartmentService = Depends(get_sys_department_service),
):
    """获取教研室与研究所部门信息分页列表"""
    result = await service.get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size,
    )


@router.get(
    "/{department_id}",
    response_model=SuccessResponse[SysDepartmentResponse],
    status_code=status.HTTP_200_OK,
    summary="获取教研室与研究所部门信息详情",
)
@handle_service_exceptions
async def get_sys_department_detail(
    department_id: int = Path(..., description="部门ID：学院下属的教研室(研究所)ID"),
    service: SysDepartmentService = Depends(get_sys_department_service),
):
    """获取教研室与研究所部门信息详情"""
    result = await service.get_detail(department_id)
    return success_response(result)


@router.post(
    "",
    response_model=SuccessResponse[SysDepartmentResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建教研室与研究所部门信息",
)
@handle_service_exceptions
async def create_sys_department(
    data: SysDepartmentCreate,
    service: SysDepartmentService = Depends(get_sys_department_service),
):
    """创建教研室与研究所部门信息"""
    result = await service.create(data)
    return success_response(result, message="教研室与研究所部门信息创建成功")


@router.put(
    "/{department_id}",
    response_model=SuccessResponse[SysDepartmentResponse],
    summary="更新教研室与研究所部门信息",
)
@handle_service_exceptions
async def update_sys_department(
    department_id: int = Path(..., description="部门ID：学院下属的教研室(研究所)ID"),
    data: SysDepartmentUpdate = ...,
    service: SysDepartmentService = Depends(get_sys_department_service),
):
    """更新教研室与研究所部门信息（不含状态/标识位字段）"""
    result = await service.update(department_id, data)
    return success_response(result, message="教研室与研究所部门信息更新成功")





@router.delete(
    "/{department_id}",
    response_model=SuccessResponse[None],
    summary="删除教研室与研究所部门信息",
)
@handle_service_exceptions
async def delete_sys_department(
    department_id: int = Path(..., description="部门ID：学院下属的教研室(研究所)ID"),
    service: SysDepartmentService = Depends(get_sys_department_service),
):
    """删除教研室与研究所部门信息"""
    await service.delete(department_id)
    return success_response(None, message="教研室与研究所部门信息删除成功")