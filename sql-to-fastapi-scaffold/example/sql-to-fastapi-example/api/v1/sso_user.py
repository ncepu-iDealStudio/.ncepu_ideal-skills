"""
用户账号信息API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from core.dependencies import get_sso_user_service
from core.database import get_db
from schemas.sso_user import SsoUserCreate, SsoUserUpdate, SsoUserResponse
from schemas.response import SuccessResponse, PaginationResponse, success_response, paginated_response
from service.sso_user_service import SsoUserService


router = APIRouter(prefix="/sso-users", tags=["用户账号信息管理"])


@router.get("", response_model=PaginationResponse[SsoUserResponse])
async def get_sso_user_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    result = get_sso_user_service(db).get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size
    )


@router.get("/{auto_id}", response_model=SuccessResponse[SsoUserResponse])
async def get_sso_user_detail(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    result = get_sso_user_service(db).get_detail(auto_id)
    return success_response(result)


@router.post("", response_model=SuccessResponse[SsoUserResponse])
async def create_sso_user(
    data: SsoUserCreate,
    db: Session = Depends(get_db)
):
    result = get_sso_user_service(db).create(data)
    return success_response(result, message="用户创建成功")


@router.put("/{auto_id}", response_model=SuccessResponse[SsoUserResponse])
async def update_sso_user(
    auto_id: int = Path(..., description="自增序号"),
    data: SsoUserUpdate = ...,
    db: Session = Depends(get_db)
):
    result = get_sso_user_service(db).update(auto_id, data)
    return success_response(result, message="用户更新成功")


@router.delete("/{auto_id}", response_model=SuccessResponse[None])
async def delete_sso_user(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    get_sso_user_service(db).delete(auto_id)
    return success_response(None, message="用户删除成功")