"""
教师API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成。

约定：
- HTTP 层统一只依赖 Service，不直接依赖 Repository。
- 字段校验由 Schema 在进入端点前完成。
"""

from fastapi import APIRouter, Depends, Path, Query, status

from core.dependencies import get_teacher_service
from service.teacher_service import TeacherService
from schemas.teacher import (
    TeacherCreate,
    TeacherUpdate,
    TeacherResponse,
    
)
from schemas.response import (
    SuccessResponse,
    PaginationResponse,
    success_response,
    paginated_response,
)
from utils.custom_exceptions import handle_service_exceptions


router = APIRouter(prefix="/teacher", tags=["教师管理"])


@router.get(
    "",
    response_model=PaginationResponse[TeacherResponse],
    status_code=status.HTTP_200_OK,
    summary="获取教师列表",
)
@handle_service_exceptions
async def get_teacher_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: TeacherService = Depends(get_teacher_service),
):
    """获取教师分页列表"""
    result = await service.get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size,
    )


@router.get(
    "/{auto_id}",
    response_model=SuccessResponse[TeacherResponse],
    status_code=status.HTTP_200_OK,
    summary="获取教师详情",
)
@handle_service_exceptions
async def get_teacher_detail(
    auto_id: int = Path(..., description="自增主键"),
    service: TeacherService = Depends(get_teacher_service),
):
    """获取教师详情"""
    result = await service.get_detail(auto_id)
    return success_response(result)


@router.post(
    "",
    response_model=SuccessResponse[TeacherResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建教师",
)
@handle_service_exceptions
async def create_teacher(
    data: TeacherCreate,
    service: TeacherService = Depends(get_teacher_service),
):
    """创建教师"""
    result = await service.create(data)
    return success_response(result, message="教师创建成功")


@router.put(
    "/{auto_id}",
    response_model=SuccessResponse[TeacherResponse],
    summary="更新教师",
)
@handle_service_exceptions
async def update_teacher(
    auto_id: int = Path(..., description="自增主键"),
    data: TeacherUpdate = ...,
    service: TeacherService = Depends(get_teacher_service),
):
    """更新教师（不含状态/标识位字段）"""
    result = await service.update(auto_id, data)
    return success_response(result, message="教师更新成功")





@router.delete(
    "/{auto_id}",
    response_model=SuccessResponse[None],
    summary="删除教师",
)
@handle_service_exceptions
async def delete_teacher(
    auto_id: int = Path(..., description="自增主键"),
    service: TeacherService = Depends(get_teacher_service),
):
    """删除教师"""
    await service.delete(auto_id)
    return success_response(None, message="教师删除成功")