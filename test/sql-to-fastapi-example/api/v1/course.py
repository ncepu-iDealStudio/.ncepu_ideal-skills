"""
课程基本信息API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from core.dependencies import get_course_service
from core.database import get_db
from schemas.course import CourseCreate, CourseUpdate, CourseResponse
from schemas.response import SuccessResponse, PaginationResponse, success_response, paginated_response
from service.course_service import CourseService


router = APIRouter(prefix="/courses", tags=["课程基本信息管理"])


@router.get("", response_model=PaginationResponse[CourseResponse])
async def get_course_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    result = get_course_service(db).get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size
    )


@router.get("/{auto_id}", response_model=SuccessResponse[CourseResponse])
async def get_course_detail(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    result = get_course_service(db).get_detail(auto_id)
    return success_response(result)


@router.post("", response_model=SuccessResponse[CourseResponse])
async def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db)
):
    result = get_course_service(db).create(data)
    return success_response(result, message="课程创建成功")


@router.put("/{auto_id}", response_model=SuccessResponse[CourseResponse])
async def update_course(
    auto_id: int = Path(..., description="自增序号"),
    data: CourseUpdate = ...,
    db: Session = Depends(get_db)
):
    result = get_course_service(db).update(auto_id, data)
    return success_response(result, message="课程更新成功")


@router.delete("/{auto_id}", response_model=SuccessResponse[None])
async def delete_course(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    get_course_service(db).delete(auto_id)
    return success_response(None, message="课程删除成功")