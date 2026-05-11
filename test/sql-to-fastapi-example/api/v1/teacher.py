"""
教师API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from core.dependencies import get_teacher_service
from core.database import get_db
from schemas.teacher import TeacherCreate, TeacherUpdate, TeacherResponse
from schemas.response import SuccessResponse, PaginationResponse, success_response, paginated_response
from service.teacher_service import TeacherService


router = APIRouter(prefix="/teachers", tags=["教师管理"])


@router.get("", response_model=PaginationResponse[TeacherResponse])
async def get_teacher_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    result = get_teacher_service(db).get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size
    )


@router.get("/{auto_id}", response_model=SuccessResponse[TeacherResponse])
async def get_teacher_detail(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    result = get_teacher_service(db).get_detail(auto_id)
    return success_response(result)


@router.post("", response_model=SuccessResponse[TeacherResponse])
async def create_teacher(
    data: TeacherCreate,
    db: Session = Depends(get_db)
):
    result = get_teacher_service(db).create(data)
    return success_response(result, message="教师创建成功")


@router.put("/{auto_id}", response_model=SuccessResponse[TeacherResponse])
async def update_teacher(
    auto_id: int = Path(..., description="自增序号"),
    data: TeacherUpdate = ...,
    db: Session = Depends(get_db)
):
    result = get_teacher_service(db).update(auto_id, data)
    return success_response(result, message="教师更新成功")


@router.delete("/{auto_id}", response_model=SuccessResponse[None])
async def delete_teacher(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    get_teacher_service(db).delete(auto_id)
    return success_response(None, message="教师删除成功")