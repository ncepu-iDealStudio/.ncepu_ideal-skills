"""
学生基本信息API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成。

约定：
- HTTP 层统一只依赖 Service，不直接依赖 Repository。
- 字段校验由 Schema 在进入端点前完成。
"""

from fastapi import APIRouter, Depends, Path, Query, status

from core.dependencies import get_student_service
from service.student_service import StudentService
from schemas.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    
)
from schemas.response import (
    SuccessResponse,
    PaginationResponse,
    success_response,
    paginated_response,
)
from utils.custom_exceptions import handle_service_exceptions


router = APIRouter(prefix="/student", tags=["学生基本信息管理"])


@router.get(
    "",
    response_model=PaginationResponse[StudentResponse],
    status_code=status.HTTP_200_OK,
    summary="获取学生基本信息列表",
)
@handle_service_exceptions
async def get_student_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: StudentService = Depends(get_student_service),
):
    """获取学生基本信息分页列表"""
    result = await service.get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size,
    )


@router.get(
    "/{auto_id}",
    response_model=SuccessResponse[StudentResponse],
    status_code=status.HTTP_200_OK,
    summary="获取学生基本信息详情",
)
@handle_service_exceptions
async def get_student_detail(
    auto_id: int = Path(..., description="自增字段"),
    service: StudentService = Depends(get_student_service),
):
    """获取学生基本信息详情"""
    result = await service.get_detail(auto_id)
    return success_response(result)


@router.post(
    "",
    response_model=SuccessResponse[StudentResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建学生基本信息",
)
@handle_service_exceptions
async def create_student(
    data: StudentCreate,
    service: StudentService = Depends(get_student_service),
):
    """创建学生基本信息"""
    result = await service.create(data)
    return success_response(result, message="学生基本信息创建成功")


@router.put(
    "/{auto_id}",
    response_model=SuccessResponse[StudentResponse],
    summary="更新学生基本信息",
)
@handle_service_exceptions
async def update_student(
    auto_id: int = Path(..., description="自增字段"),
    data: StudentUpdate = ...,
    service: StudentService = Depends(get_student_service),
):
    """更新学生基本信息（不含状态/标识位字段）"""
    result = await service.update(auto_id, data)
    return success_response(result, message="学生基本信息更新成功")





@router.delete(
    "/{auto_id}",
    response_model=SuccessResponse[None],
    summary="删除学生基本信息",
)
@handle_service_exceptions
async def delete_student(
    auto_id: int = Path(..., description="自增字段"),
    service: StudentService = Depends(get_student_service),
):
    """删除学生基本信息"""
    await service.delete(auto_id)
    return success_response(None, message="学生基本信息删除成功")