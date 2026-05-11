"""
课程安排API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from core.dependencies import get_course_arrangement_service
from core.database import get_db
from schemas.course_arrangement import CourseArrangementCreate, CourseArrangementUpdate, CourseArrangementResponse
from schemas.response import SuccessResponse, PaginationResponse, success_response, paginated_response
from service.course_arrangement_service import CourseArrangementService


router = APIRouter(prefix="/course-arrangements", tags=["课程安排管理"])


@router.get("", response_model=PaginationResponse[CourseArrangementResponse])
async def get_course_arrangement_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    result = get_course_arrangement_service(db).get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size
    )


@router.get("/{auto_id}", response_model=SuccessResponse[CourseArrangementResponse])
async def get_course_arrangement_detail(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    result = get_course_arrangement_service(db).get_detail(auto_id)
    return success_response(result)


@router.post("", response_model=SuccessResponse[CourseArrangementResponse])
async def create_course_arrangement(
    data: CourseArrangementCreate,
    db: Session = Depends(get_db)
):
    result = get_course_arrangement_service(db).create(data)
    return success_response(result, message="课程安排创建成功")


@router.put("/{auto_id}", response_model=SuccessResponse[CourseArrangementResponse])
async def update_course_arrangement(
    auto_id: int = Path(..., description="自增序号"),
    data: CourseArrangementUpdate = ...,
    db: Session = Depends(get_db)
):
    result = get_course_arrangement_service(db).update(auto_id, data)
    return success_response(result, message="课程安排更新成功")


@router.delete("/{auto_id}", response_model=SuccessResponse[None])
async def delete_course_arrangement(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    get_course_arrangement_service(db).delete(auto_id)
    return success_response(None, message="课程安排删除成功")