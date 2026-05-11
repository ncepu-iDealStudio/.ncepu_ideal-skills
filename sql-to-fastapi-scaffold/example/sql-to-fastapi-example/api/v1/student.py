"""
学生基本信息API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from core.dependencies import get_student_service
from core.database import get_db
from schemas.student import StudentCreate, StudentUpdate, StudentResponse
from schemas.response import SuccessResponse, PaginationResponse, success_response, paginated_response
from service.student_service import StudentService


router = APIRouter(prefix="/students", tags=["学生基本信息管理"])


@router.get("", response_model=PaginationResponse[StudentResponse])
async def get_student_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    result = get_student_service(db).get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size
    )


@router.get("/{auto_id}", response_model=SuccessResponse[StudentResponse])
async def get_student_detail(
    auto_id: int = Path(..., description="自增字段"),
    db: Session = Depends(get_db)
):
    result = get_student_service(db).get_detail(auto_id)
    return success_response(result)


@router.post("", response_model=SuccessResponse[StudentResponse])
async def create_student(
    data: StudentCreate,
    db: Session = Depends(get_db)
):
    result = get_student_service(db).create(data)
    return success_response(result, message="学生创建成功")


@router.put("/{auto_id}", response_model=SuccessResponse[StudentResponse])
async def update_student(
    auto_id: int = Path(..., description="自增字段"),
    data: StudentUpdate = ...,
    db: Session = Depends(get_db)
):
    result = get_student_service(db).update(auto_id, data)
    return success_response(result, message="学生更新成功")


@router.delete("/{auto_id}", response_model=SuccessResponse[None])
async def delete_student(
    auto_id: int = Path(..., description="自增字段"),
    db: Session = Depends(get_db)
):
    get_student_service(db).delete(auto_id)
    return success_response(None, message="学生删除成功")