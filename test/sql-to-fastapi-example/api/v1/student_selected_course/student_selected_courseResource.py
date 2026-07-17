"""
学生选课情况API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成。

约定：
- HTTP 层统一只依赖 Service，不直接依赖 Repository。
- 字段校验由 Schema 在进入端点前完成。
"""

from fastapi import APIRouter, Depends, Path, Query, status

from core.dependencies import get_student_selected_course_service
from service.student_selected_course_service import StudentSelectedCourseService
from schemas.student_selected_course import (
    StudentSelectedCourseCreate,
    StudentSelectedCourseUpdate,
    StudentSelectedCourseResponse,
    
)
from schemas.response import (
    SuccessResponse,
    PaginationResponse,
    success_response,
    paginated_response,
)
from utils.custom_exceptions import handle_service_exceptions


router = APIRouter(prefix="/student-selected-course", tags=["学生选课情况管理"])


@router.get(
    "",
    response_model=PaginationResponse[StudentSelectedCourseResponse],
    status_code=status.HTTP_200_OK,
    summary="获取学生选课情况列表",
)
@handle_service_exceptions
async def get_student_selected_course_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    service: StudentSelectedCourseService = Depends(get_student_selected_course_service),
):
    """获取学生选课情况分页列表"""
    result = await service.get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size,
    )


@router.get(
    "/{auto_id}",
    response_model=SuccessResponse[StudentSelectedCourseResponse],
    status_code=status.HTTP_200_OK,
    summary="获取学生选课情况详情",
)
@handle_service_exceptions
async def get_student_selected_course_detail(
    auto_id: int = Path(..., description="自增序号字段"),
    service: StudentSelectedCourseService = Depends(get_student_selected_course_service),
):
    """获取学生选课情况详情"""
    result = await service.get_detail(auto_id)
    return success_response(result)


@router.post(
    "",
    response_model=SuccessResponse[StudentSelectedCourseResponse],
    status_code=status.HTTP_201_CREATED,
    summary="创建学生选课情况",
)
@handle_service_exceptions
async def create_student_selected_course(
    data: StudentSelectedCourseCreate,
    service: StudentSelectedCourseService = Depends(get_student_selected_course_service),
):
    """创建学生选课情况"""
    result = await service.create(data)
    return success_response(result, message="学生选课情况创建成功")


@router.put(
    "/{auto_id}",
    response_model=SuccessResponse[StudentSelectedCourseResponse],
    summary="更新学生选课情况",
)
@handle_service_exceptions
async def update_student_selected_course(
    auto_id: int = Path(..., description="自增序号字段"),
    data: StudentSelectedCourseUpdate = ...,
    service: StudentSelectedCourseService = Depends(get_student_selected_course_service),
):
    """更新学生选课情况（不含状态/标识位字段）"""
    result = await service.update(auto_id, data)
    return success_response(result, message="学生选课情况更新成功")





@router.delete(
    "/{auto_id}",
    response_model=SuccessResponse[None],
    summary="删除学生选课情况",
)
@handle_service_exceptions
async def delete_student_selected_course(
    auto_id: int = Path(..., description="自增序号字段"),
    service: StudentSelectedCourseService = Depends(get_student_selected_course_service),
):
    """删除学生选课情况"""
    await service.delete(auto_id)
    return success_response(None, message="学生选课情况删除成功")