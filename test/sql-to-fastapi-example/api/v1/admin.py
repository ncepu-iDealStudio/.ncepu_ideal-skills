"""
管理员API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from core.dependencies import get_admin_service
from core.database import get_db
from schemas.admin import AdminCreate, AdminUpdate, AdminResponse
from schemas.response import SuccessResponse, PaginationResponse, success_response, paginated_response
from service.admin_service import AdminService


router = APIRouter(prefix="/admins", tags=["管理员管理"])


@router.get("", response_model=PaginationResponse[AdminResponse])
async def get_admin_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    result = get_admin_service(db).get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size
    )


@router.get("/{auto_id}", response_model=SuccessResponse[AdminResponse])
async def get_admin_detail(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    result = get_admin_service(db).get_detail(auto_id)
    return success_response(result)


@router.post("", response_model=SuccessResponse[AdminResponse])
async def create_admin(
    data: AdminCreate,
    db: Session = Depends(get_db)
):
    result = get_admin_service(db).create(data)
    return success_response(result, message="管理员创建成功")


@router.put("/{auto_id}", response_model=SuccessResponse[AdminResponse])
async def update_admin(
    auto_id: int = Path(..., description="自增序号"),
    data: AdminUpdate = ...,
    db: Session = Depends(get_db)
):
    result = get_admin_service(db).update(auto_id, data)
    return success_response(result, message="管理员更新成功")


@router.delete("/{auto_id}", response_model=SuccessResponse[None])
async def delete_admin(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    get_admin_service(db).delete(auto_id)
    return success_response(None, message="管理员删除成功")