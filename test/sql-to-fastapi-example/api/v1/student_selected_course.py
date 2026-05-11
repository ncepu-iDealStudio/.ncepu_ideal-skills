"""
学生选课情况API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from core.dependencies import get_student_selected_course_service
from core.database import get_db
from schemas.student_selected_course import StudentSelectedCourseCreate, StudentSelectedCourseUpdate, StudentSelectedCourseResponse
from schemas.response import SuccessResponse, PaginationResponse, success_response, paginated_response
from service.student_selected_course_service import StudentSelectedCourseService


router = APIRouter(prefix="/student-selected-courses", tags=["学生选课情况管理"])


@router.get("", response_model=PaginationResponse[StudentSelectedCourseResponse])
async def get_student_selected_course_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    result = get_student_selected_course_service(db).get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size
    )


@router.get("/{auto_id}", response_model=SuccessResponse[StudentSelectedCourseResponse])
async def get_student_selected_course_detail(
    auto_id: int = Path(..., description="自增序号字段"),
    db: Session = Depends(get_db)
):
    result = get_student_selected_course_service(db).get_detail(auto_id)
    return success_response(result)


@router.post("", response_model=SuccessResponse[StudentSelectedCourseResponse])
async def create_student_selected_course(
    data: StudentSelectedCourseCreate,
    db: Session = Depends(get_db)
):
    result = get_student_selected_course_service(db).create(data)
    return success_response(result, message="学生选课记录创建成功")


@router.put("/{auto_id}", response_model=SuccessResponse[StudentSelectedCourseResponse])
async def update_student_selected_course(
    auto_id: int = Path(..., description="自增序号字段"),
    data: StudentSelectedCourseUpdate = ...,
    db: Session = Depends(get_db)
):
    result = get_student_selected_course_service(db).update(auto_id, data)
    return success_response(result, message="学生选课记录更新成功")


@router.delete("/{auto_id}", response_model=SuccessResponse[None])
async def delete_student_selected_course(
    auto_id: int = Path(..., description="自增序号字段"),
    db: Session = Depends(get_db)
):
    get_student_selected_course_service(db).delete(auto_id)
    return success_response(None, message="学生选课记录删除成功")