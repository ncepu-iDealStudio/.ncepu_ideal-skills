"""
班级信息业务服务

此文件由 SQL-to-FastAPI-Scaffold 自动生成
"""

from typing import Dict
from sqlalchemy.orm import Session

from models.sys_class_info import SysClassInfo
from schemas.sys_class_info import SysClassInfoCreate, SysClassInfoUpdate, SysClassInfoResponse
from utils.custom_exceptions import BadRequestException, NotFoundException


class SysClassInfoService:
    """
    班级信息服务类
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SysClassInfoCreate) -> SysClassInfoResponse:
        obj_data = data.model_dump(exclude={"auto_id"})
        obj = SysClassInfo(**obj_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return SysClassInfoResponse.model_validate(obj)

    def get_list(self, page: int, size: int) -> Dict:
        query = self.db.query(SysClassInfo).filter(SysClassInfo.is_deleted == False)

        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()

        return {
            "items": [SysClassInfoResponse.model_validate(item) for item in items],
            "total": total
        }

    def get_detail(self, auto_id: int) -> SysClassInfoResponse:
        obj = self.db.query(SysClassInfo).filter(
            SysClassInfo.auto_id == auto_id,
            SysClassInfo.is_deleted == False
        ).first()

        if not obj:
            raise NotFoundException("班级不存在")

        return SysClassInfoResponse.model_validate(obj)

    def update(self, auto_id: int, data: SysClassInfoUpdate) -> SysClassInfoResponse:
        obj = self.db.query(SysClassInfo).filter(
            SysClassInfo.auto_id == auto_id,
            SysClassInfo.is_deleted == False
        ).first()

        if not obj:
            raise NotFoundException("班级不存在")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        self.db.commit()
        self.db.refresh(obj)

        return SysClassInfoResponse.model_validate(obj)

    def delete(self, auto_id: int) -> None:
        obj = self.db.query(SysClassInfo).filter(
            SysClassInfo.auto_id == auto_id,
            SysClassInfo.is_deleted == False
        ).first()

        if not obj:
            raise NotFoundException("班级不存在")

        setattr(obj, "is_deleted", True)
        self.db.commit()