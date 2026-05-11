"""
教研室与研究所信息API路由

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from core.dependencies import get_sys_department_info_service
from core.database import get_db
from schemas.sys_department_info import SysDepartmentInfoCreate, SysDepartmentInfoUpdate, SysDepartmentInfoResponse
from schemas.response import SuccessResponse, PaginationResponse, success_response, paginated_response
from service.sys_department_info_service import SysDepartmentInfoService


router = APIRouter(prefix="/sys-department-infos", tags=["教研室与研究所信息管理"])


@router.get("", response_model=PaginationResponse[SysDepartmentInfoResponse])
async def get_sys_department_info_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    result = get_sys_department_info_service(db).get_list(page=page, size=page_size)
    return paginated_response(
        items=result["items"],
        total=result["total"],
        page=page,
        size=page_size
    )


@router.get("/{auto_id}", response_model=SuccessResponse[SysDepartmentInfoResponse])
async def get_sys_department_info_detail(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    result = get_sys_department_info_service(db).get_detail(auto_id)
    return success_response(result)


@router.post("", response_model=SuccessResponse[SysDepartmentInfoResponse])
async def create_sys_department_info(
    data: SysDepartmentInfoCreate,
    db: Session = Depends(get_db)
):
    result = get_sys_department_info_service(db).create(data)
    return success_response(result, message="部门创建成功")


@router.put("/{auto_id}", response_model=SuccessResponse[SysDepartmentInfoResponse])
async def update_sys_department_info(
    auto_id: int = Path(..., description="自增序号"),
    data: SysDepartmentInfoUpdate = ...,
    db: Session = Depends(get_db)
):
    result = get_sys_department_info_service(db).update(auto_id, data)
    return success_response(result, message="部门更新成功")


@router.delete("/{auto_id}", response_model=SuccessResponse[None])
async def delete_sys_department_info(
    auto_id: int = Path(..., description="自增序号"),
    db: Session = Depends(get_db)
):
    get_sys_department_info_service(db).delete(auto_id)
    return success_response(None, message="部门删除成功")