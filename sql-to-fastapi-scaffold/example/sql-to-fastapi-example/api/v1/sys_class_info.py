"""
班级信息API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from core.dependencies import get_sys_class_info_service
from core.database import get_db
from schemas.sys_class_info import SysClassInfoCreate, SysClassInfoUpdate, SysClassInfoResponse
from schemas.response import SuccessResponse, PaginationResponse, success_response, paginated_response
from service.sys_class_info_service import SysClassInfoService


router = APIRouter(prefix="/sys-class-infos", tags=["班级信息管理"])


@router.get("", response_model=PaginationResponse[SysClassInfoResponse])
async def get_sys_class_info_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    result = get_sys_class_info_service(db).get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size
    )


@router.get("/{auto_id}", response_model=SuccessResponse[SysClassInfoResponse])
async def get_sys_class_info_detail(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    result = get_sys_class_info_service(db).get_detail(auto_id)
    return success_response(result)


@router.post("", response_model=SuccessResponse[SysClassInfoResponse])
async def create_sys_class_info(
    data: SysClassInfoCreate,
    db: Session = Depends(get_db)
):
    result = get_sys_class_info_service(db).create(data)
    return success_response(result, message="班级创建成功")


@router.put("/{auto_id}", response_model=SuccessResponse[SysClassInfoResponse])
async def update_sys_class_info(
    auto_id: int = Path(..., description="自增序号"),
    data: SysClassInfoUpdate = ...,
    db: Session = Depends(get_db)
):
    result = get_sys_class_info_service(db).update(auto_id, data)
    return success_response(result, message="班级更新成功")


@router.delete("/{auto_id}", response_model=SuccessResponse[None])
async def delete_sys_class_info(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    get_sys_class_info_service(db).delete(auto_id)
    return success_response(None, message="班级删除成功")