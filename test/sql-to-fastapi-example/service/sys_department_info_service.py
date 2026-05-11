"""
教研室与研究所信息业务服务

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Dict
from sqlalchemy.orm import Session

from models.sys_department_info import SysDepartmentInfo
from schemas.sys_department_info import SysDepartmentInfoCreate, SysDepartmentInfoUpdate, SysDepartmentInfoResponse
from utils.custom_exceptions import BadRequestException, NotFoundException


class SysDepartmentInfoService:
    """
    教研室与研究所信息服务类
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SysDepartmentInfoCreate) -> SysDepartmentInfoResponse:
        obj_data = data.model_dump(exclude={"auto_id"})
        obj = SysDepartmentInfo(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return SysDepartmentInfoResponse.model_validate(obj)

    def get_list(self, page: int, size: int) -> Dict:
        query = self.db.query(SysDepartmentInfo).filter(SysDepartmentInfo.is_deleted == False)

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()

        return {
            "items": [SysDepartmentInfoResponse.model_validate(item) for item in items],
            "total": total
        }

    def get_detail(self, auto_id: int) -> SysDepartmentInfoResponse:
        obj = self.db.query(SysDepartmentInfo).filter(
            SysDepartmentInfo.auto_id == auto_id,
            SysDepartmentInfo.is_deleted == False
        ).first()

        if not obj:
            raise NotFoundException("部门不存在")

        return SysDepartmentInfoResponse.model_validate(obj)

    def update(self, auto_id: int, data: SysDepartmentInfoUpdate) -> SysDepartmentInfoResponse:
        obj = self.db.query(SysDepartmentInfo).filter(
            SysDepartmentInfo.auto_id == auto_id,
            SysDepartmentInfo.is_deleted == False
        ).first()

        if not obj:
            raise NotFoundException("部门不存在")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return SysDepartmentInfoResponse.model_validate(obj)

    def delete(self, auto_id: int) -> None:
        obj = self.db.query(SysDepartmentInfo).filter(
            SysDepartmentInfo.auto_id == auto_id,
            SysDepartmentInfo.is_deleted == False
        ).first()

        if not obj:
            raise NotFoundException("部门不存在")

        setattr(obj, "is_deleted", True)
        self.db.commit()