"""
课程安排API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成。

约定：
- HTTP 层统一只依赖 Service，不直接依赖 Repository。
- 字段校验由 Schema 在进入端点前完成。
"""

from fastapi import APIRouter, Depends, Path, Query, status

from core.dependencies import get_course_arrangement_service
from service.course_arrangement_service import CourseArrangementService
from schemas.course_arrangement import (
    CourseArrangementCreate,
    CourseArrangementUpdate,
    CourseArrangementResponse,
    
)
from schemas.response import (
    SuccessResponse,
    PaginationResponse,
    success_response,
    paginated_response,
)
from utils.custom_exceptions import handle_service_exceptions


router = APIRouter(prefix="/course-arrangement", tags=["课程安排管理"])


@router.get(
    "",
    response_model=PaginationResponse[CourseArrangementResponse],
    status_code=status.HTTP_200_OK,
    summary="获取课程安排列表",
)
@handle_service_exceptions
async def get_course_arrangement_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: CourseArrangementService = Depends(get_course_arrangement_service),
):
    """获取课程安排分页列表"""
    result = await service.get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size,
    )


@router.get(
    "/{auto_id}",
    response_model=SuccessResponse[CourseArrangementResponse],
    status_code=status.HTTP_200_OK,
    summary="获取课程安排详情",
)
@handle_service_exceptions
async def get_course_arrangement_detail(
    auto_id: int = Path(..., description="自增序号"),
    service: CourseArrangementService = Depends(get_course_arrangement_service),
):
    """获取课程安排详情"""
    result = await service.get_detail(auto_id)
    return success_response(result)


@router.post(
    "",
    response_model=SuccessResponse[CourseArrangementResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建课程安排",
)
@handle_service_exceptions
async def create_course_arrangement(
    data: CourseArrangementCreate,
    service: CourseArrangementService = Depends(get_course_arrangement_service),
):
    """创建课程安排"""
    result = await service.create(data)
    return success_response(result, message="课程安排创建成功")


@router.put(
    "/{auto_id}",
    response_model=SuccessResponse[CourseArrangementResponse],
    summary="更新课程安排",
)
@handle_service_exceptions
async def update_course_arrangement(
    auto_id: int = Path(..., description="自增序号"),
    data: CourseArrangementUpdate = ...,
    service: CourseArrangementService = Depends(get_course_arrangement_service),
):
    """更新课程安排（不含状态/标识位字段）"""
    result = await service.update(auto_id, data)
    return success_response(result, message="课程安排更新成功")





@router.delete(
    "/{auto_id}",
    response_model=SuccessResponse[None],
    summary="删除课程安排",
)
@handle_service_exceptions
async def delete_course_arrangement(
    auto_id: int = Path(..., description="自增序号"),
    service: CourseArrangementService = Depends(get_course_arrangement_service),
):
    """删除课程安排"""
    await service.delete(auto_id)
    return success_response(None, message="课程安排删除成功")